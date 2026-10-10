@echo off
rem Stage 2: all command-line parameters
cd /d "%~dp0.."
echo ===== no parameters
echo exit | python src\emulator.py
echo ===== --help
python src\emulator.py --help
echo ===== --vfs
echo exit | python src\emulator.py --vfs C:\vfs\data
echo ===== --script
python src\emulator.py --script scripts\ok.txt
echo ===== --vfs and --script
python src\emulator.py --vfs C:\vfs\data --script scripts\ok.txt
echo exit code: %errorlevel%
echo ===== unknown parameter
python src\emulator.py --oops
