# IntelliVuln Hub - Server Startup Script
# Run this script to start both backend and frontend servers

Write-Host "🚀 Starting IntelliVuln Hub Servers..." -ForegroundColor Cyan
Write-Host ""

# Add Node.js to PATH
$env:Path += ";C:\Program Files\nodejs"

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Backend directory
$backendDir = Join-Path $scriptDir "backend"

# Frontend directory (current directory)
$frontendDir = $scriptDir

Write-Host "📂 Backend Directory: $backendDir" -ForegroundColor Gray
Write-Host "📂 Frontend Directory: $frontendDir" -ForegroundColor Gray
Write-Host ""

# Start Backend Server
Write-Host "🔧 Starting Backend Server (FastAPI)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendDir'; Write-Host '🐍 Activating Python Virtual Environment...' -ForegroundColor Green; .\venv\Scripts\Activate.ps1; Write-Host '🚀 Starting Backend on http://localhost:8000' -ForegroundColor Green; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

Start-Sleep -Seconds 2

# Start Frontend Server
Write-Host "🔧 Starting Frontend Server (Vite)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:Path += ';C:\Program Files\nodejs'; cd '$frontendDir'; Write-Host '⚡ Starting Frontend on http://localhost:8080' -ForegroundColor Green; npm run dev"

Write-Host ""
Write-Host "✅ Servers are starting in separate windows!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Server URLs:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:8080" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "⏰ Wait 5-10 seconds for servers to fully start..." -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 Opening browser in 8 seconds..." -ForegroundColor Cyan

Start-Sleep -Seconds 8

# Open browser
Start-Process "http://localhost:8080"

Write-Host ""
Write-Host "✨ All done! Check the other PowerShell windows for server logs." -ForegroundColor Green
Write-Host "   Press Ctrl+C in each window to stop the servers." -ForegroundColor Gray
Write-Host ""
