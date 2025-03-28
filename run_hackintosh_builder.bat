@echo off
echo Hackintosh EFI Builder Launcher
echo ==============================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if resources exist, if not generate them
if not exist resources\app_icon.png (
    echo Generating resources...
    python generate_resources.py
)

REM Check if dependencies are installed
echo Checking dependencies...
pip show customtkinter > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies.
        echo Please run 'pip install -r requirements.txt' manually.
        pause
        exit /b 1
    )
)

REM Run the application
echo Starting Hackintosh EFI Builder...
python main.py

exit /b 0