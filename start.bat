@echo off
title Video Script Generator - Starting Services
color 0A

echo ========================================
echo   Video Script Generator Bot
echo   Starting Frontend and Backend
echo ========================================
echo.

REM Check if Python is installed (try multiple commands)
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
) else (
    python3 --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=python3
    ) else (
        py --version >nul 2>&1
        if not errorlevel 1 (
            set PYTHON_CMD=py
        )
    )
)

if "%PYTHON_CMD%"=="" (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please do ONE of the following:
    echo.
    echo Option 1: Install Python from https://www.python.org
    echo   - Download Python 3.8 or newer
    echo   - IMPORTANT: Check "Add Python to PATH" during installation
    echo   - Restart your computer after installation
    echo.
    echo Option 2: If Python is already installed, add it to PATH:
    echo   - Search for "Environment Variables" in Windows
    echo   - Edit "Path" variable
    echo   - Add Python installation folder (e.g., C:\Python39)
    echo   - Add Python Scripts folder (e.g., C:\Python39\Scripts)
    echo   - Restart command prompt
    echo.
    echo Option 3: Use Python Launcher (py command):
    echo   - Install Python from Microsoft Store
    echo   - Or install Python with "py launcher" option
    echo.
    pause
    exit /b 1
) else (
    echo [OK] Python found: %PYTHON_CMD%
    %PYTHON_CMD% --version
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

REM Check if Ollama is running
echo [1/4] Checking Ollama connection...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:11434/api/tags' -TimeoutSec 2 -UseBasicParsing; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama does not appear to be running
    echo Please start Ollama by running: ollama serve
    echo Or make sure Ollama is installed from https://ollama.com
    echo.
    echo Press any key to continue anyway, or Ctrl+C to exit...
    pause >nul
) else (
    echo [OK] Ollama is running
)

REM Check if backend dependencies are installed
echo [2/4] Checking backend dependencies...
cd backend
if not exist "venv\" (
    echo Backend virtual environment not found. Creating...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        echo Trying alternative method...
        %PYTHON_CMD% -m virtualenv venv
        if errorlevel 1 (
            echo [ERROR] Failed to create virtual environment
            echo Please install virtualenv: %PYTHON_CMD% -m pip install virtualenv
            cd ..
            pause
            exit /b 1
        )
    )
)
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    python -c "import flask" >nul 2>&1
    if errorlevel 1 (
        echo Installing backend dependencies...
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
        if errorlevel 1 (
            echo [ERROR] Failed to install backend dependencies
            echo Please check requirements.txt and try installing manually:
            echo   cd backend
            echo   venv\Scripts\activate
            echo   pip install -r requirements.txt
            cd ..
            pause
            exit /b 1
        )
    ) else (
        echo [OK] Backend dependencies are installed
    )
) else (
    echo [ERROR] Virtual environment activation script not found
    echo The venv folder exists but activate.bat is missing.
    echo Try deleting the venv folder and running this script again.
    cd ..
    pause
    exit /b 1
)
cd ..

REM Check if frontend dependencies are installed
echo [3/4] Checking frontend dependencies...
cd frontend
if not exist "node_modules\" (
    echo Frontend dependencies not found. Installing...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies
        cd ..
        pause
        exit /b 1
    )
)
cd ..

REM Start backend server
echo [4/4] Starting services...
echo.
echo ========================================
echo   Backend Server (Flask)
echo ========================================
start "Backend Server" cmd /k "cd backend && call venv\Scripts\activate.bat && python app.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend server
echo ========================================
echo   Frontend Server (React/Vite)
echo ========================================
start "Frontend Server" cmd /k "cd frontend && npm run dev"

REM Wait a bit for frontend to start
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   Services Started Successfully!
echo ========================================
echo.
echo   Frontend URL: http://localhost:3000
echo   Backend API:  http://localhost:5000
echo.
echo   Both servers are running in separate windows.
echo   Close those windows to stop the servers.
echo.
echo   Press any key to open the frontend in your browser...
pause >nul

REM Open browser
start http://localhost:3000

echo.
echo Browser opened! The application should be loading...
echo.
echo To stop the servers, close the "Backend Server" and "Frontend Server" windows.
echo.
pause
