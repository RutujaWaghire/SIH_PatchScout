# PatchScout Setup Instructions

## ⚠️ Critical First Steps

Your system needs Node.js to run the frontend. Here's how to get everything working:

## Step 1: Install Node.js (REQUIRED)

### Option A: Using winget (Recommended for Windows 11)
```powershell
winget install OpenJS.NodeJS.LTS
```

### Option B: Manual Download
1. Visit: https://nodejs.org/en/download/
2. Download "LTS" version for Windows (20.x or 18.x)
3. Run the installer with default options
4. Restart PowerShell after installation

### Verify Installation
After installing, open a NEW PowerShell window and run:
```powershell
node --version
npm --version
```
You should see version numbers (e.g., v20.11.0 and 10.2.4).

## Step 2: Install Frontend Dependencies

Once Node.js is installed, navigate to your project folder:
```powershell
cd "c:\Users\Atharv Danave\Downloads\intellivuln-hub-main\intellivuln-hub-main"
npm install
```

This will install all frontend dependencies (React, TypeScript, Vite, etc.).

## Step 3: Install Python (if not already installed)

### Check if Python is installed:
```powershell
python --version
```

### If not installed:
1. Visit: https://www.python.org/downloads/
2. Download Python 3.11 or 3.12
3. **Important**: Check "Add Python to PATH" during installation
4. Restart PowerShell

## Step 4: Install Backend Dependencies

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Step 5: Install Docker Desktop (for databases)

1. Visit: https://www.docker.com/products/docker-desktop/
2. Download and install Docker Desktop for Windows
3. Start Docker Desktop
4. Wait for it to fully start (whale icon in system tray)

## Step 6: Start Backend Services

In PowerShell (from backend directory):
```powershell
docker-compose up -d postgres redis neo4j
```

This starts:
- PostgreSQL (database) on port 5432
- Redis (caching) on port 6379
- Neo4j (graph database) on ports 7474/7687

## Step 7: Setup Environment Variables

Copy the example environment file:
```powershell
Copy-Item .env.example .env
```

Edit `.env` and update any API keys (NVD, etc.) if you have them.

## Step 8: Initialize Database

```powershell
# Still in backend directory with venv activated
python -c "from app.database import init_db; init_db()"
```

## Step 9: Start the Application

### Terminal 1 - Backend:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend (NEW PowerShell window):
```powershell
cd "c:\Users\Atharv Danave\Downloads\intellivuln-hub-main\intellivuln-hub-main"
npm run dev
```

## Step 10: Access the Application

- Frontend: http://localhost:8080 (or port shown by Vite)
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Neo4j Browser: http://localhost:7474

## Common Issues & Solutions

### Issue: "node is not recognized"
**Solution**: You need to install Node.js (see Step 1). After installation, restart PowerShell.

### Issue: "python is not recognized"
**Solution**: Install Python and ensure "Add to PATH" was checked during installation.

### Issue: "docker-compose: command not found"
**Solution**: Install Docker Desktop and ensure it's running.

### Issue: Module import errors in backend
**Solution**: Make sure you activated the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```

### Issue: Frontend compilation errors
**Solution**: Delete `node_modules` and reinstall:
```powershell
Remove-Item -Recurse -Force node_modules
npm install
```

### Issue: Port already in use
**Solution**: Change ports in `vite.config.ts` (frontend) or `backend/app/config.py` (backend).

## Architecture Overview

```
PatchScout
├── Frontend (React + TypeScript + Vite)
│   ├── Port: 8080 (default Vite port)
│   ├── UI: Shadcn/ui components
│   └── State: TanStack Query
│
├── Backend (FastAPI + Python)
│   ├── Port: 8000
│   ├── API: REST + WebSocket
│   └── Services: Scanning, AI/RAG, Threat Intel
│
└── Databases (Docker Containers)
    ├── PostgreSQL: Port 5432 (relational data)
    ├── Neo4j: Ports 7474/7687 (attack graphs)
    ├── Redis: Port 6379 (caching)
    └── ChromaDB: Embedded (vector store)
```

## Next Steps After Setup

1. **Test the Scanner**: Use the Scanner tab to run Nmap scans
2. **View Dashboard**: Check vulnerability metrics and charts
3. **Explore Attack Paths**: Visualize attack chains in graph view
4. **Try AI Assistant**: Ask questions about vulnerabilities
5. **Review Threat Intel**: See global threat landscape

## Development Workflow

### Making Frontend Changes:
1. Edit files in `src/`
2. Vite will hot-reload automatically
3. Check browser console for errors

### Making Backend Changes:
1. Edit files in `backend/app/`
2. Uvicorn will auto-reload (if `--reload` flag is used)
3. Check API docs at http://localhost:8000/docs

### Database Migrations:
```powershell
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Security Notes

- The `.env` file contains sensitive credentials - never commit it to Git
- Change default passwords in `docker-compose.yml` for production
- Enable HTTPS in production environments
- Set `DEBUG=False` in production

## Support

If you encounter issues:
1. Check logs: `docker-compose logs` (for services)
2. Check API logs: Terminal running uvicorn
3. Check browser console: F12 in browser
4. Review error messages carefully

## Installation Checklist

- [ ] Node.js installed and verified (`node --version`)
- [ ] Frontend dependencies installed (`npm install` successful)
- [ ] Python installed and verified (`python --version`)
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Docker Desktop installed and running
- [ ] Database containers started (`docker-compose up -d`)
- [ ] Environment variables configured (`.env` file)
- [ ] Database initialized
- [ ] Backend server running (port 8000)
- [ ] Frontend dev server running (port 8080)
- [ ] Application accessible in browser

---

**You are currently at**: Step 1 - Need to install Node.js

**Your next action**: Run `winget install OpenJS.NodeJS.LTS` or download from nodejs.org, then restart PowerShell and run `npm install` in the project directory.
