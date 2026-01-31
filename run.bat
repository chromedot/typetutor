@echo off
REM Run script for Typing Tutor application (development mode)

echo Starting Typing Tutor...
echo.

REM Activate virtual environment and run
call venv\Scripts\activate.bat
python src\main.py

pause
