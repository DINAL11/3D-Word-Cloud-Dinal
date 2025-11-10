#!/bin/bash

# 3D Word Cloud Project Setup Script (Unix/Mac/Linux)
# This script installs dependencies and starts both frontend and backend servers

set -e  # Exit on error

echo "=================================="
echo "3D Word Cloud - Project Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo "✓ Node.js found: $(node --version)"
echo ""

# Backend setup
echo "=================================="
echo "Setting up Backend..."
echo "=================================="
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK data
echo "Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('punkt_tab', quiet=True)"

echo "✓ Backend setup complete!"
echo ""

# Return to root directory
cd ..

# Frontend setup
echo "=================================="
echo "Setting up Frontend..."
echo "=================================="
cd frontend

# Install Node dependencies
echo "Installing Node dependencies..."
npm install

echo "✓ Frontend setup complete!"
echo ""

# Return to root directory
cd ..

# Start servers
echo "=================================="
echo "Starting Servers..."
echo "=================================="
echo ""
echo "Backend will start on: http://localhost:8000"
echo "Frontend will start on: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to kill all background processes on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $(jobs -p) 2>/dev/null || true
    exit
}

trap cleanup INT TERM

# Start backend in background
cd backend
source venv/bin/activate
uvicorn main:app --reload &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend in foreground
cd frontend
npm run dev

# If frontend exits, cleanup
cleanup