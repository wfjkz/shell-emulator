@echo off
rem Stage 1: REPL demo with all commands and errors
cd /d "%~dp0.."
(
echo ls
echo ls -l /home
echo cd /tmp
echo cd a b
echo unknown arg1 arg2
echo exit 1 2
echo exit abc
echo exit 5
) | python src\emulator.py
echo exit code: %errorlevel%
