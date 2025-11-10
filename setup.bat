@echo off
REM 3D Word Cloud Project Setup Script (Windows)
REM This script installs dependencies and starts both frontend and backend servers

echo ==================================
echo 3D Word Cloud - Project Setup
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)

echo Python found
python --version
echo Node.js found
node --version
echo.

REM Backend setup
echo ==================================
echo Setting up Backend...
echo ==================================
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Download NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('punkt_tab', quiet=True)"

echo Backend setup complete!
echo.

REM Return to root directory
cd ..

REM Frontend setup
echo ==================================
echo Setting up Frontend...
echo ==================================
cd frontend

REM Install Node dependencies
echo Installing Node dependencies...
call npm install

echo Frontend setup complete!
echo.

REM Return to root directory
cd ..

REM Start servers
echo ==================================
echo Starting Servers...
echo ==================================
echo.
echo Backend will start on: http://localhost:8000
echo Frontend will start on: http://localhost:5173
echo.
echo Press Ctrl+C to stop both servers
echo.

REM Start backend in new window
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate.bat && uvicorn main:app --reload"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend in new window
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting in separate windows!
echo Close those windows to stop the servers.
echo.
pause