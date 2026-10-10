"""Эмулятор командной оболочки UNIX-подобной ОС (вариант 16)."""

import argparse
import getpass
import socket
import sys


class CommandError(Exception):
    """Ошибка выполнения команды."""


class Emulator:
    """Консольный эмулятор оболочки."""

    def __init__(self, vfs_path=None, script_path=None):
        """Сохраняет параметры и берёт имя пользователя и хоста из ОС."""
        self.vfs_path = vfs_path
        self.script_path = script_path
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.running = True
        self.exit_code = 0
        self.commands = {
            "ls": self.ls,
            "cd": self.cd,
            "exit": self.exit,
        }

    def prompt(self):
        """Приглашение вида username@hostname:~$."""
        return f"{self.user}@{self.host}:~$ "

    @staticmethod
    def parse(line):
        """Делит ввод на команду и аргументы по пробелам."""
        parts = line.split()
        if not parts:
            return None, []
        return parts[0], parts[1:]

    def ls(self, args):
        """Заглушка ls: печатает имя и аргументы."""
        print(f"ls: args={args}")

    def cd(self, args):
        """Заглушка cd: печатает имя и аргументы, принимает один путь."""
        if len(args) > 1:
            raise CommandError("cd: too many arguments")
        print(f"cd: args={args}")

    def exit(self, args):
        """exit [код] — завершает работу эмулятора."""
        if len(args) > 1:
            raise CommandError("exit: too many arguments")
        if args and not args[0].isdigit():
            raise CommandError(f"exit: {args[0]}: numeric argument required")
        self.exit_code = int(args[0]) if args else 0
        self.running = False

    def execute(self, line):
        """Выполняет строку; возвращает True при успехе."""
        name, args = self.parse(line)
        if name is None:
            return True
        handler = self.commands.get(name)
        try:
            if handler is None:
                raise CommandError(f"{name}: command not found")
            handler(args)
        except CommandError as error:
            print(f"error: {error}")
            return False
        return True

    def print_config(self):
        """Отладочный вывод всех параметров запуска."""
        print("=== emulator config ===")
        print(f"VFS path    : {self.vfs_path}")
        print(f"Script path : {self.script_path}")
        print(f"User / host : {self.user} / {self.host}")
        print("=======================")

    def run_script(self):
        """Выполняет стартовый скрипт до первой ошибки.

        Каждая команда печатается после приглашения, затем её вывод.
        Возвращает True, если скрипт выполнен без ошибок.
        """
        try:
            with open(self.script_path, encoding="utf-8") as file:
                lines = file.read().splitlines()
        except OSError as error:
            print(f"error: cannot open script '{self.script_path}': "
                  f"{error.strerror}")
            return False
        for number, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            print(self.prompt() + line)
            if not self.execute(line):
                print(f"error: script stopped at line {number}")
                return False
            if not self.running:
                break
        return True

    def run(self):
        """Выполняет стартовый скрипт (если задан) и интерактивный цикл."""
        self.print_config()
        if self.script_path and not self.run_script():
            return 1
        while self.running:
            try:
                line = input(self.prompt())
            except EOFError:
                print()
                break
            self.execute(line)
        return self.exit_code


def parse_arguments(argv=None):
    """Разбирает параметры командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки UNIX")
    parser.add_argument("--vfs", help="путь к физическому расположению VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args(argv)


if __name__ == "__main__":
    options = parse_arguments()
    sys.exit(Emulator(options.vfs, options.script).run())
