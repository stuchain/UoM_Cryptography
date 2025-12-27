#!/bin/bash
# Run the demo (macOS/Linux)

echo "============================================================"
echo "Secure Channel Demo - Simple Launcher"
echo "============================================================"
echo ""

# Python check
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.10+ from: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo "[OK] Python found"
python3 --version

# Run from repo root
if [ ! -f "requirements.txt" ]; then
    echo "[ERROR] requirements.txt not found!"
    echo "Please run this script from the project root directory."
    echo ""
    exit 1
fi

# Dependencies
echo ""
echo "Checking dependencies..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "[INFO] Installing dependencies (this may take a minute)..."
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies!"
        echo "Please check your internet connection and try again."
        echo ""
        exit 1
    fi
    echo "[OK] Dependencies installed successfully!"
else
    echo "[OK] Dependencies already installed"
fi

# Sanity checks
if [ ! -d "backend" ]; then
    echo "[ERROR] backend directory not found!"
    exit 1
fi

if [ ! -f "backend/app.py" ]; then
    echo "[ERROR] app.py not found in backend directory!"
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo "[ERROR] frontend directory not found!"
    exit 1
fi

if [ ! -f "frontend/templates/index.html" ]; then
    echo "[ERROR] index.html not found in frontend/templates directory!"
    exit 1
fi

echo ""
echo "============================================================"
echo "Starting Flask server..."
echo "============================================================"
echo ""
echo "The server will start at: http://localhost:5000"
echo ""
echo "Your browser should open automatically."
echo "If not, manually open: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

# Open the browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    sleep 3
    open http://localhost:5000
# Linux
elif command -v xdg-open &> /dev/null; then
    sleep 3
    xdg-open http://localhost:5000 &
fi

# Start server
cd backend
python3 app.py

