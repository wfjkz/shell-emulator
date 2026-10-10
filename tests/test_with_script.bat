@echo off
rem Stage 2: script stops at the first error
cd /d "%~dp0.."
echo ===== correct script
python src\emulator.py --script scripts\ok.txt
echo exit code: %errorlevel%
echo ===== script with error
python src\emulator.py --script scripts\fail.txt
echo exit code: %errorlevel%
echo ===== missing script
python src\emulator.py --script scripts\missing.txt
echo exit code: %errorlevel%
