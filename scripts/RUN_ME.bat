@echo off
REM Enhanced launcher - keeps window open and shows all output
title Secure Channel Demo Launcher

REM Make sure we're in the right directory
cd /d "%~dp0"

REM Clear screen and show header
cls
echo.
echo ============================================================
echo    SECURE CHANNEL DEMO - LAUNCHER
echo ============================================================
echo.
echo Starting up... Please wait...
echo.
echo Current folder: %CD%
echo.

REM Test Python first
echo [1/5] Checking Python installation...
python --version 2>nul
if errorlevel 1 (
    cls
    echo.
    echo ============================================================
    echo ERROR: Python not found!
    echo ============================================================
    echo.
    echo Python is not installed or not in your PATH.
    echo.
    echo Please:
    echo 1. Install Python 3.10+ from https://www.python.org/downloads/
    echo 2. During installation, CHECK "Add Python to PATH"
    echo 3. Restart your computer after installation
    echo 4. Try running this script again
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
python --version
echo [OK] Python found!
echo.

REM Check requirements.txt
echo [2/5] Checking project files...
if not exist "requirements.txt" (
    cls
    echo.
    echo ============================================================
    echo ERROR: Project files not found!
    echo ============================================================
    echo.
    echo Cannot find requirements.txt
    echo Current folder: %CD%
    echo.
    echo Make sure you're running this from the project root folder.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
echo [OK] Project files found!
echo.

REM Check dependencies
echo [3/5] Checking dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [INFO] Dependencies not installed. Installing now...
    echo This may take a few minutes. Please wait...
    echo.
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        cls
        echo.
        echo ============================================================
        echo ERROR: Failed to install dependencies!
        echo ============================================================
        echo.
        echo Please check your internet connection and try again.
        echo Or install manually: pip install -r requirements.txt
        echo.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    )
    echo [OK] Dependencies installed!
) else (
    echo [OK] Dependencies already installed!
)
echo.

REM Check frontend
echo [4/5] Checking frontend...
if not exist "frontend\app.py" (
    cls
    echo.
    echo ============================================================
    echo ERROR: Frontend not found!
    echo ============================================================
    echo.
    echo Cannot find frontend\app.py
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
echo [OK] Frontend found!
echo.

REM Start server
echo [5/5] Starting server...
echo.
echo ============================================================
echo    SERVER STARTING
echo ============================================================
echo.
echo The web interface will open in your browser at:
echo    http://localhost:5000
echo.
echo The server window will stay open while running.
echo Press Ctrl+C to stop the server when done.
echo.
echo ============================================================
echo.

REM Wait and open browser
timeout /t 2 /nobreak >nul
start http://localhost:5000

REM Start Flask
cd frontend
python app.py

REM If server stops
echo.
echo.
echo ============================================================
echo Server has stopped.
echo ============================================================
echo.
pause

