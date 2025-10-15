# PatchScout - Complete Setup Script for Windows
# This script will check and install all requirements

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   PatchScout - Complete Setup Script" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0
$WarningCount = 0

# Function to check if command exists
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction SilentlyContinue) {
            return $true
        }
    } catch {}
    return $false
}

# Check Node.js
Write-Host "[1/6] Checking Node.js..." -ForegroundColor Yellow
if (Test-Command "node") {
    $nodeVersion = node --version
    Write-Host "  ✓ Node.js is installed: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Node.js is NOT installed" -ForegroundColor Red
    Write-Host "  Please install from: https://nodejs.org/" -ForegroundColor Yellow
    $ErrorCount++
}

# Check Python
Write-Host "[2/6] Checking Python..." -ForegroundColor Yellow
if (Test-Command "python") {
    $pythonVersion = python --version
    Write-Host "  ✓ Python is installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python is NOT installed" -ForegroundColor Red
    Write-Host "  Please install from: https://python.org/" -ForegroundColor Yellow
    Write-Host "  Make sure to check 'Add Python to PATH'" -ForegroundColor Yellow
    $ErrorCount++
}

# Check Nmap
Write-Host "[3/6] Checking Nmap..." -ForegroundColor Yellow
if (Test-Command "nmap") {
    $nmapVersion = nmap --version | Select-Object -First 1
    Write-Host "  ✓ Nmap is installed: $nmapVersion" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Nmap is NOT installed (optional but recommended)" -ForegroundColor Yellow
    Write-Host "  Download from: https://nmap.org/download.html" -ForegroundColor Yellow
    $WarningCount++
}

# Check Docker
Write-Host "[4/6] Checking Docker..." -ForegroundColor Yellow
if (Test-Command "docker") {
    $dockerVersion = docker --version
    Write-Host "  ✓ Docker is installed: $dockerVersion" -ForegroundColor Green
    
    # Check if Docker is running
    try {
        docker ps | Out-Null
        Write-Host "  ✓ Docker is running" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ Docker is installed but not running" -ForegroundColor Yellow
        Write-Host "  Please start Docker Desktop" -ForegroundColor Yellow
        $WarningCount++
    }
} else {
    Write-Host "  ⚠ Docker is NOT installed (optional)" -ForegroundColor Yellow
    Write-Host "  Download from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    $WarningCount++
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   Installation Summary" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

if ($ErrorCount -eq 0) {
    Write-Host "✓ All required dependencies are installed!" -ForegroundColor Green
    
    if ($WarningCount -gt 0) {
        Write-Host "⚠ $WarningCount optional dependencies are missing" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "   Next Steps" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Frontend Setup
    Write-Host "[5/6] Setting up Frontend..." -ForegroundColor Yellow
    if (Test-Path "node_modules") {
        Write-Host "  ✓ Frontend dependencies already installed" -ForegroundColor Green
    } else {
        Write-Host "  Installing frontend dependencies..." -ForegroundColor Cyan
        npm install
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Frontend dependencies installed successfully" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Failed to install frontend dependencies" -ForegroundColor Red
        }
    }
    
    # Backend Setup
    Write-Host "[6/6] Setting up Backend..." -ForegroundColor Yellow
    Push-Location backend
    
    if (Test-Path "venv") {
        Write-Host "  ✓ Virtual environment already exists" -ForegroundColor Green
    } else {
        Write-Host "  Creating Python virtual environment..." -ForegroundColor Cyan
        python -m venv venv
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
        }
    }
    
    Write-Host "  Activating virtual environment..." -ForegroundColor Cyan
    & .\venv\Scripts\Activate.ps1
    
    Write-Host "  Installing Python dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Python dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Some Python dependencies may have failed" -ForegroundColor Yellow
    }
    
    # Create .env if not exists
    if (!(Test-Path ".env")) {
        Copy-Item .env.example .env
        Write-Host "  ✓ Created .env file" -ForegroundColor Green
    }
    
    Pop-Location
    
    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "   🎉 Setup Complete!" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To start the application:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Start Backend (in new terminal):" -ForegroundColor Yellow
    Write-Host "   cd backend" -ForegroundColor White
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Start Frontend (in this terminal):" -ForegroundColor Yellow
    Write-Host "   npm run dev" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Open in browser:" -ForegroundColor Yellow
    Write-Host "   http://localhost:8080" -ForegroundColor White
    Write-Host ""
    Write-Host "Optional - Start Databases:" -ForegroundColor Yellow
    Write-Host "   cd backend" -ForegroundColor White
    Write-Host "   docker-compose up -d postgres redis neo4j" -ForegroundColor White
    Write-Host ""
    
} else {
    Write-Host "✗ $ErrorCount required dependencies are missing!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install the missing dependencies and run this script again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Quick Install Commands:" -ForegroundColor Cyan
    Write-Host "  Node.js:  winget install OpenJS.NodeJS.LTS" -ForegroundColor White
    Write-Host "  Python:   winget install Python.Python.3.11" -ForegroundColor White
    Write-Host "  Nmap:     winget install Insecure.Nmap" -ForegroundColor White
    Write-Host ""
}

Write-Host "For detailed documentation, see:" -ForegroundColor Cyan
Write-Host "  - SETUP_INSTRUCTIONS.md" -ForegroundColor White
Write-Host "  - BACKEND_READY.md" -ForegroundColor White
Write-Host "  - STATIC_VS_DYNAMIC.md" -ForegroundColor White
Write-Host ""
