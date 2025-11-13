# Simple PowerShell launcher script for Secure Channel Demo
# This script checks dependencies and starts the frontend automatically

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Secure Channel Demo - Simple Launcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.10+ from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "requirements.txt")) {
    Write-Host "[ERROR] requirements.txt not found!" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if dependencies are installed
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Cyan
try {
    python -c "import flask" 2>&1 | Out-Null
    Write-Host "[OK] Dependencies already installed" -ForegroundColor Green
} catch {
    Write-Host "[INFO] Installing dependencies (this may take a minute)..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
        Write-Host "Please check your internet connection and try again." -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[OK] Dependencies installed successfully!" -ForegroundColor Green
}

# Navigate to frontend directory
if (-not (Test-Path "frontend")) {
    Write-Host "[ERROR] frontend directory not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path "frontend\app.py")) {
    Write-Host "[ERROR] app.py not found in frontend directory!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting Flask server..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The server will start at: http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "Your browser should open automatically." -ForegroundColor Yellow
Write-Host "If not, manually open: http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Wait a moment then open browser
Start-Sleep -Seconds 3
Start-Process "http://localhost:5000"

# Start the Flask server
Set-Location frontend
python app.py

