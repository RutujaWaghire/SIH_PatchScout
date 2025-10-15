# 🔍 Troubleshooting Black Screen Issue

## Issue: Black screen when starting a scan

This happens when the frontend encounters an error but doesn't handle it gracefully.

## Quick Diagnostics

### Step 1: Open Browser Developer Tools
1. Open http://localhost:8080 in your browser
2. Press **F12** or **Right-click → Inspect**
3. Go to **Console** tab
4. Click **Scanner** tab
5. Enter a target (e.g., `scanme.nmap.org`)
6. Click **Start Scan**
7. **Look for red error messages in console**

### Step 2: Check Network Tab
1. In Developer Tools, go to **Network** tab
2. Try to start scan again
3. Look for failed requests (shown in red)
4. Click on the failed request
5. Check the **Response** tab to see the error

---

## Common Causes & Fixes

### 1. Backend Not Responding
**Symptoms**: Console shows `Failed to fetch` or `net::ERR_CONNECTION_REFUSED`

**Fix**: Make sure backend is running
```powershell
# In backend terminal, check if you see:
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. CORS Error
**Symptoms**: Console shows `CORS policy` or `Access-Control-Allow-Origin`

**Fix**: Backend .env needs correct CORS settings
```env
CORS_ORIGINS=["http://localhost:8080", "http://localhost:5173"]
```

### 3. API Route Mismatch
**Symptoms**: Console shows `404 Not Found`

**Fix**: Check if API is accessible at http://localhost:8000/api/scans/

### 4. Missing Nmap
**Symptoms**: Backend logs show `Nmap not found` or `command not found`

**Fix**: Install Nmap
- Windows: https://nmap.org/download.html
- After installing, restart backend

---

## Immediate Fix

Let me create a better error-handling version of the Scanner component:

### Option A: Check Backend Health First

Open http://localhost:8000/docs in your browser and:
1. Expand **POST /api/scans/**
2. Click **Try it out**
3. Enter test data:
```json
{
  "target": "scanme.nmap.org",
  "scan_config": {
    "selected_tools": ["Nmap"],
    "scan_type": "quick",
    "aggressiveness": "medium",
    "port_range": "1-1000",
    "include_nse": false,
    "compliance": []
  }
}
```
4. Click **Execute**
5. Check if you get a response

### Option B: Simplify Scanner

I'll create a minimal working scanner that shows proper errors instead of black screen.

---

## Most Likely Issue

Based on the code, the black screen happens because:

1. **Frontend makes API call** → `api.createScan()`
2. **API call fails** (backend not responding, CORS, or error)
3. **Error is caught** but page doesn't show error message properly
4. **React component crashes** → Black screen

The fix is to add a fallback error UI.

---

## Next Step

Please do this:

1. **Open browser** → http://localhost:8080
2. **Press F12** → Open Console tab
3. **Try to scan** → Enter any website and click Start
4. **Copy the error message** from console (the red text)
5. **Paste it here** so I can see the exact error

This will tell me exactly what's failing!

---

## Quick Test

Try this in your browser console (F12 → Console tab):
```javascript
fetch('http://localhost:8000/api/scans/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    target: 'scanme.nmap.org',
    scan_config: {
      selected_tools: ['Nmap'],
      scan_type: 'quick',
      aggressiveness: 'medium',
      port_range: '1-1000',
      include_nse: false,
      compliance: []
    }
  })
})
.then(r => r.json())
.then(d => console.log('Success:', d))
.catch(e => console.error('Error:', e))
```

This will test if the API is reachable!
