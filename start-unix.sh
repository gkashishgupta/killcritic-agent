#!/bin/bash
# KILLCRITIC - macOS/Linux Startup Script
# This script installs dependencies and starts the backend server

echo ""
echo "========================================"
echo "  KILLCRITIC - Startup Idea Analyzer"
echo "========================================"
echo ""

# Navigate to backend folder
cd backend

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error installing dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "   Starting KILLCRITIC Backend..."
echo "========================================"
echo ""
echo "Frontend: Open frontend/index.html in your browser"
echo "API: http://localhost:5000"
echo ""

python3 app.py
