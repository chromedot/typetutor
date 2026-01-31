@echo off
REM Build script for Typing Tutor application

echo Building Typing Tutor executable...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build with PyInstaller
pyinstaller typing_tutor.spec

echo.
if exist dist\TypingTutor.exe (
    echo Build successful!
    echo Executable created at: dist\TypingTutor.exe
) else (
    echo Build failed. Please check the error messages above.
)

pause
