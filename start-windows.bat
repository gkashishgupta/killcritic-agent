@echo off
REM KILLCRITIC - Windows Startup Script
REM This script installs dependencies and starts the backend server

echo.
echo ========================================
echo   KILLCRITIC - Startup Idea Analyzer
echo ========================================
echo.

REM Navigate to backend folder
cd backend

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Starting KILLCRITIC Backend...
echo ========================================
echo.
echo Frontend: Open frontend/index.html in your browser
echo API: http://localhost:5000
echo.

python app.py

pause
