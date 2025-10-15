# 🌍 Share Over Internet - ngrok Setup Guide

Your friend is **NOT on the same Wi-Fi**, so we'll use **ngrok** to create a public tunnel.

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Download ngrok

1. Go to: **https://ngrok.com/download**
2. Click **"Download for Windows"**
3. Extract the ZIP file to a folder (e.g., `C:\ngrok\`)

---

### Step 2: Sign Up (Free)

1. Go to: **https://dashboard.ngrok.com/signup**
2. Sign up with Google/GitHub (fastest) or email
3. After signup, you'll see your **Authtoken** on the dashboard

---

### Step 3: Configure ngrok

Open PowerShell and run:

```powershell
# Navigate to where you extracted ngrok
cd C:\ngrok

# Add your authtoken (replace YOUR_TOKEN with actual token from dashboard)
.\ngrok.exe config add-authtoken YOUR_TOKEN_HERE
```

**Example:**
```powershell
.\ngrok.exe config add-authtoken 2abc123def456ghi789jkl0mno1pqr2s3t4u5v6w7x8y9z
```

---

### Step 4: Start ngrok Tunnel

Keep your servers running, then in a **NEW PowerShell window**:

```powershell
cd C:\ngrok
.\ngrok.exe http 8080
```

You'll see output like this:
```
ngrok

Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123xyz.ngrok-free.app -> http://localhost:8080

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

---

### Step 5: Share the Link!

**Look for the "Forwarding" line** and copy the **https** URL.

**Example:** `https://abc123xyz.ngrok-free.app`

**Send this link to your friend!** They can access it from anywhere in the world! 🌍

---

## 📱 Message to Send Your Friend

```
Hey! Check out my security scanner project:

🔗 https://abc123xyz.ngrok-free.app
(Replace with YOUR actual ngrok URL)

This works from anywhere - no need to be on my network!

Try:
- Dashboard (view security stats)
- Scanner tab (scan: scanme.nmap.org)
- AI Assistant (ask security questions)
- Analyzer (view vulnerability reports)

Note: The link only works while I'm running the servers.
Let me know what you think! 🚀
```

---

## 🎯 Complete PowerShell Commands

### Terminal 1: Backend (Already Running)
```powershell
cd "C:\Users\Atharv Danave\Downloads\intellivuln-hub-main\intellivuln-hub-main\backend"
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Frontend (Already Running)
```powershell
cd "C:\Users\Atharv Danave\Downloads\intellivuln-hub-main\intellivuln-hub-main"
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
npm run dev
```

### Terminal 3: ngrok (NEW - Run This Now)
```powershell
cd C:\ngrok
.\ngrok.exe http 8080
```

---

## 🔧 Troubleshooting

### Problem: "command not found"
**Solution:** Make sure you're in the ngrok folder:
```powershell
cd C:\ngrok
.\ngrok.exe http 8080
```

### Problem: "authentication required"
**Solution:** Add your authtoken:
```powershell
.\ngrok.exe config add-authtoken YOUR_TOKEN_FROM_DASHBOARD
```

### Problem: Backend API not working
**Solution:** You need to tunnel BOTH ports. See "Advanced Setup" below.

---

## 🚀 Advanced Setup (If Backend Issues)

If your friend sees the website but features don't work, you need to tunnel the backend too.

### Option 1: Use ngrok Free Plan (2 Tunnels)

**Terminal 3: Frontend Tunnel**
```powershell
cd C:\ngrok
.\ngrok.exe http 8080
```

**Terminal 4: Backend Tunnel (NEW)**
```powershell
cd C:\ngrok
.\ngrok.exe http 8000
```

You'll get TWO URLs:
- Frontend: `https://abc123.ngrok-free.app`
- Backend: `https://def456.ngrok-free.app`

### Option 2: Update Frontend to Use ngrok Backend

If features don't work, you may need to update the API URL in the frontend.

**Don't worry about this unless your friend reports issues!**

---

## ⚙️ ngrok Features

### Free Plan Includes:
- ✅ Public HTTPS URL
- ✅ Works from anywhere in the world
- ✅ No firewall configuration needed
- ✅ Automatic HTTPS certificate
- ⚠️ URL changes each time you restart ngrok
- ⚠️ Limited to 1 connection at a time (free plan)

### Paid Plans ($8/month):
- Custom domain names
- Multiple simultaneous connections
- More regions
- Better performance

---

## 🌐 What Your Friend Will See

1. **Click your ngrok link**
2. May see ngrok warning page (click "Visit Site")
3. Your IntelliVuln Hub dashboard appears!
4. Full functionality works

---

## 📊 Monitor Traffic

ngrok provides a web interface to see all requests:

**Open in your browser:**
```
http://localhost:4040
```

You can see:
- All HTTP requests from your friend
- Response times
- Request/response details

---

## ⏹️ Stop Sharing

When done:
1. Press `Ctrl+C` in the ngrok terminal
2. The tunnel stops immediately
3. Your friend can no longer access

---

## 🔒 Security Notes

### ⚠️ Important:
- ngrok URL is public - anyone with the link can access
- Free plan shows "ngrok" branding page first
- Don't share sensitive data through ngrok free tier
- URL is temporary and changes on restart

### ✅ Safe for:
- Demos and presentations
- Showing projects to friends
- Testing with remote users
- Short-term sharing

### ❌ Not recommended for:
- Production applications
- Sensitive customer data
- Long-term hosting
- Business-critical apps

---

## 🎬 For Your Demo

ngrok is PERFECT for showing your project because:
- ✅ Your friend can access from anywhere
- ✅ No network configuration needed
- ✅ Automatic HTTPS (looks professional!)
- ✅ Easy to start/stop
- ✅ Free for demos

---

## 💡 Alternative Methods

If ngrok doesn't work:

### Option 1: Cloudflare Tunnel (Free)
```powershell
# Download cloudflared
# Run: cloudflared tunnel --url http://localhost:8080
```

### Option 2: Localtunnel
```powershell
npm install -g localtunnel
lt --port 8080
```

### Option 3: Deploy to Cloud (Permanent)
- **Vercel** (Frontend) - Free
- **Render** (Full stack) - Free tier
- **Railway** (Full stack) - Free trial

---

## ✅ Quick Checklist

Before starting ngrok:
- [ ] Backend running on port 8000
- [ ] Frontend running on port 8080
- [ ] ngrok downloaded and extracted
- [ ] ngrok authtoken configured
- [ ] New PowerShell window ready

To share:
- [ ] Run: `ngrok http 8080`
- [ ] Copy the https URL
- [ ] Send to friend
- [ ] Keep terminal open while sharing

---

## 🚀 FASTEST WAY TO START

### 1. Download ngrok:
```
https://ngrok.com/download
```

### 2. Extract to C:\ngrok\

### 3. Get your token:
```
https://dashboard.ngrok.com/get-started/your-authtoken
```

### 4. Run these commands:
```powershell
cd C:\ngrok
.\ngrok.exe config add-authtoken YOUR_TOKEN
.\ngrok.exe http 8080
```

### 5. Copy the https URL and send to your friend!

---

**That's it! Your friend can now access from anywhere!** 🌍✨

The URL will look like: `https://abc123xyz.ngrok-free.app`

Keep the ngrok terminal open while your friend is viewing!
