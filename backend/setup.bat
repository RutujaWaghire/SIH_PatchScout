@echo off
REM PatchScout Backend Setup Script for Windows

echo ================================================
echo  PatchScout Backend Setup
echo ================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo [✓] Python found

REM Create virtual environment
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
    echo [✓] Virtual environment created
) else (
    echo [✓] Virtual environment already exists
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [*] Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "chroma_db" mkdir chroma_db
if not exist "model_cache" mkdir model_cache

REM Copy environment file
if not exist ".env" (
    echo [*] Creating .env file from template...
    copy .env.example .env
    echo [!] Please edit .env file with your configuration
)

echo.
echo ================================================
echo  Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Install Docker Desktop and run: docker-compose up -d
echo 3. Run: python scripts\init_db.py
echo 4. Start server: uvicorn app.main:app --reload
echo.
echo API Documentation: http://localhost:8000/docs
echo.
pause
