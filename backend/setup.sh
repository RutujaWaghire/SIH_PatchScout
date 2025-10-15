#!/bin/bash
# PatchScout Backend Setup Script for Linux/Mac

set -e

echo "================================================"
echo " PatchScout Backend Setup"
echo "================================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.9+ first"
    exit 1
fi

echo "[✓] Python found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
    echo "[✓] Virtual environment created"
else
    echo "[✓] Virtual environment already exists"
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "[*] Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "[*] Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs chroma_db model_cache

# Copy environment file
if [ ! -f ".env" ]; then
    echo "[*] Creating .env file from template..."
    cp .env.example .env
    echo "[!] Please edit .env file with your configuration"
fi

echo ""
echo "================================================"
echo " Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Start Docker services: docker-compose up -d"
echo "3. Initialize database: python scripts/init_db.py"
echo "4. Start server: uvicorn app.main:app --reload"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo ""
