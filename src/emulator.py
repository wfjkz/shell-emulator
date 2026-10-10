"""Эмулятор командной оболочки UNIX-подобной ОС (вариант 16)."""

import getpass
import socket
import sys


class CommandError(Exception):
    """Ошибка выполнения команды."""


class Emulator:
    """Консольный эмулятор оболочки."""

    def __init__(self):
        """Определяет имя пользователя и компьютера из реальной ОС."""
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

    def run(self):
        """Интерактивный цикл чтения и выполнения команд."""
        while self.running:
            try:
                line = input(self.prompt())
            except EOFError:
                print()
                break
            self.execute(line)
        return self.exit_code


if __name__ == "__main__":
    sys.exit(Emulator().run())
