# PatchScout - Quick Start Script
# Starts both backend and frontend servers

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  PatchScout - Quick Start" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if running in correct directory
if (-Not (Test-Path "package.json")) {
    Write-Host "Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Function to start backend
function Start-Backend {
    Write-Host "[Backend] Starting FastAPI server..." -ForegroundColor Green
    Set-Location backend
    
    # Check if venv exists
    if (-Not (Test-Path "venv")) {
        Write-Host "[Backend] Virtual environment not found. Run setup-complete.ps1 first!" -ForegroundColor Red
        Set-Location ..
        return
    }
    
    # Start backend in new window
    Start-Process powershell -ArgumentList @(
        "-NoExit",
        "-Command",
        "& {
            Write-Host '================================' -ForegroundColor Cyan;
            Write-Host '  PatchScout Backend Server' -ForegroundColor Cyan;
            Write-Host '================================' -ForegroundColor Cyan;
            Write-Host '';
            Write-Host 'API Server: http://localhost:8000' -ForegroundColor Green;
            Write-Host 'API Docs: http://localhost:8000/docs' -ForegroundColor Green;
            Write-Host '';
            Write-Host 'Press Ctrl+C to stop' -ForegroundColor Yellow;
            Write-Host '';
            .\venv\Scripts\Activate.ps1;
            uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        }"
    )
    
    Set-Location ..
}

# Function to start frontend
function Start-Frontend {
    Write-Host "[Frontend] Starting Vite dev server..." -ForegroundColor Green
    
    # Check if node_modules exists
    if (-Not (Test-Path "node_modules")) {
        Write-Host "[Frontend] Dependencies not installed. Run setup-complete.ps1 first!" -ForegroundColor Red
        return
    }
    
    Start-Sleep -Seconds 3  # Wait for backend to start
    
    # Start frontend in new window
    Start-Process powershell -ArgumentList @(
        "-NoExit",
        "-Command",
        "& {
            Write-Host '================================' -ForegroundColor Cyan;
            Write-Host '  PatchScout Frontend Server' -ForegroundColor Cyan;
            Write-Host '================================' -ForegroundColor Cyan;
            Write-Host '';
            Write-Host 'Application: http://localhost:8080' -ForegroundColor Green;
            Write-Host '';
            Write-Host 'Press Ctrl+C to stop' -ForegroundColor Yellow;
            Write-Host '';
            npm run dev
        }"
    )
}

# Main execution
Write-Host "🚀 Starting PatchScout..." -ForegroundColor Cyan
Write-Host ""

# Start backend
Start-Backend

# Wait a bit
Write-Host ""
Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start frontend
Start-Frontend

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ PatchScout Started!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access Points:" -ForegroundColor Cyan
Write-Host "  • Frontend: http://localhost:8080" -ForegroundColor White
Write-Host "  • Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "  • API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Two new PowerShell windows have opened for backend and frontend." -ForegroundColor Yellow
Write-Host "Close those windows to stop the servers." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
