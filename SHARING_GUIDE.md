# 🌐 Sharing IntelliVuln Hub with Your Friend

## 📱 Quick Links to Share

### If Your Friend is on the SAME Wi-Fi Network:

**Share these URLs:**
```
Frontend (Main Website): http://192.168.0.145:8080
Backend API: http://192.168.0.145:8000
API Documentation: http://192.168.0.145:8000/docs
```

### Alternative Network Interface:
```
http://192.168.56.1:8080
```

---

## ✅ Prerequisites - What Your Friend Needs

1. **Same Wi-Fi Network**: Your friend must be connected to the **same Wi-Fi** as you
2. **Firewall**: Windows Firewall must allow connections (see instructions below)
3. **Servers Running**: Keep both backend and frontend servers running on your PC

---

## 🔥 Step 1: Configure Windows Firewall (IMPORTANT!)

Your friend won't be able to connect unless you allow these ports through Windows Firewall.

### Option A: Quick Command (Run as Administrator)

Open PowerShell **as Administrator** and run:

```powershell
# Allow port 8080 (Frontend)
New-NetFirewallRule -DisplayName "IntelliVuln Frontend" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow

# Allow port 8000 (Backend)
New-NetFirewallRule -DisplayName "IntelliVuln Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### Option B: Manual Configuration (GUI Method)

1. Press `Win + R`, type `wf.msc`, press Enter
2. Click **"Inbound Rules"** in left panel
3. Click **"New Rule..."** in right panel
4. Select **"Port"**, click Next
5. Select **"TCP"**, enter **"8080"**, click Next
6. Select **"Allow the connection"**, click Next
7. Check all profiles (Domain, Private, Public), click Next
8. Name: **"IntelliVuln Frontend"**, click Finish
9. **Repeat steps 3-8 for port 8000** (name it "IntelliVuln Backend")

---

## 📋 Step 2: Share the Links

### Send Your Friend This Message:

```
Hey! I'm sharing my security scanner project with you.

🌐 Access it here: http://192.168.0.145:8080

Make sure you're on my Wi-Fi network!

What you can do:
- View the security dashboard
- Run vulnerability scans (use target: scanme.nmap.org)
- Analyze security reports
- Chat with the AI Security Assistant

Let me know if it doesn't load!
```

---

## 🧪 Step 3: Test the Connection Yourself First

Before your friend tries, test it from your phone (connected to same Wi-Fi):

### On Your Phone:
1. Connect to the same Wi-Fi
2. Open browser
3. Go to: `http://192.168.0.145:8080`
4. You should see the IntelliVuln Hub dashboard

**If it works on your phone, it will work for your friend!**

---

## 🔍 Troubleshooting Guide

### Problem 1: "Site Can't Be Reached"

**Solution A - Check Firewall:**
```powershell
# Check if firewall rules exist
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*IntelliVuln*"}
```

**Solution B - Temporarily Disable Firewall (Testing Only):**
```powershell
# ⚠️ ONLY FOR TESTING - Re-enable after!
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# To re-enable:
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

**Solution C - Check Servers are Running:**
```powershell
netstat -ano | findstr "LISTENING" | findstr ":8000 :8080"
```
You should see both ports listed.

### Problem 2: Backend API Not Working

Your friend might see the website but features don't work.

**Check Backend is Accessible:**
Ask your friend to visit: `http://192.168.0.145:8000/docs`

They should see the API documentation page.

**If not working:**
- Port 8000 firewall rule not set
- Backend server crashed (check your terminal)

### Problem 3: Different Wi-Fi Networks

If your friend is NOT on the same Wi-Fi, you need to:

1. **Use ngrok** (tunneling service) - See section below
2. **Set up port forwarding** on your router
3. **Deploy to a cloud server** (Heroku, AWS, etc.)

---

## 🌍 Sharing Over the Internet (Not Same Wi-Fi)

If your friend is on a different network, use **ngrok**:

### Step 1: Install ngrok

1. Go to: https://ngrok.com/download
2. Download and extract ngrok
3. Sign up for free account
4. Copy your auth token from dashboard

### Step 2: Setup ngrok

```powershell
# Authenticate
.\ngrok.exe config add-authtoken YOUR_AUTH_TOKEN_HERE

# Create tunnel for frontend
.\ngrok.exe http 8080
```

### Step 3: Share the Link

ngrok will display something like:
```
Forwarding: https://abc123.ngrok.io -> http://localhost:8080
```

**Share this link**: `https://abc123.ngrok.io`

Your friend can access it from anywhere in the world!

### Step 4: Backend Tunnel (If Needed)

In a **separate PowerShell window**:
```powershell
.\ngrok.exe http 8000
```

You'll need to update the frontend API URL to use the ngrok backend URL.

---

## ⚙️ Configuration for Network Access

### Frontend Configuration

The frontend is already configured to work on your network because Vite uses `0.0.0.0` by default.

### Backend Configuration

The backend is running with `--host 0.0.0.0` which allows network access.

**Current command:**
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The `--host 0.0.0.0` means "accept connections from any IP address".

---

## 📊 Network Information

### Your Computer's IP Addresses:
- **Wi-Fi**: 192.168.0.145 (Use this for sharing!)
- **Virtual Adapter**: 192.168.56.1

### Servers Status:
- ✅ **Frontend**: Running on 0.0.0.0:8080 (accessible from network)
- ✅ **Backend**: Running on 0.0.0.0:8000 (accessible from network)

### Share These URLs:
```
Main Website: http://192.168.0.145:8080
API Docs:     http://192.168.0.145:8000/docs
```

---

## 🛡️ Security Considerations

### ⚠️ Important Notes:

1. **Only share on trusted networks** (your home Wi-Fi)
2. **Don't expose to public internet** without authentication
3. **Firewall rules persist** - Remove them when done:
   ```powershell
   Remove-NetFirewallRule -DisplayName "IntelliVuln Frontend"
   Remove-NetFirewallRule -DisplayName "IntelliVuln Backend"
   ```

4. **Stop servers when done** - Press `Ctrl+C` in both PowerShell windows

### Best Practices:

✅ **Only share with trusted friends**
✅ **Use temporary firewall rules**
✅ **Stop servers when not in use**
✅ **Monitor your terminal logs** for suspicious activity
❌ **Don't share your database** (backend/patchscout.db)
❌ **Don't expose to public internet** without proper security

---

## 📱 Quick Share Checklist

Before your friend connects:

- [ ] Both servers running (backend + frontend)
- [ ] Firewall rules created for ports 8000 and 8080
- [ ] Tested on your phone first
- [ ] Confirmed your IP: 192.168.0.145
- [ ] Friend connected to same Wi-Fi network
- [ ] Shared the link: http://192.168.0.145:8080

---

## 🎬 For Video Sharing

If you want to share a video of the project instead:

### Option 1: Record Video
- Use OBS Studio or Windows Game Bar (Win + G)
- Upload to YouTube/Google Drive
- Share the video link

### Option 2: Screenshots
- Take screenshots of key features
- Upload to Imgur or Google Drive
- Share the image link

### Option 3: Live Stream (Advanced)
- Use Discord screen share
- Use Zoom and share screen
- Use Google Meet

---

## 💡 Alternative: Deploy to Cloud

For permanent sharing, deploy to:

### Free Options:
1. **Vercel** (Frontend only) - https://vercel.com
2. **Render** (Backend + Frontend) - https://render.com
3. **Railway** (Full stack) - https://railway.app
4. **Fly.io** (Full stack) - https://fly.io

I can help you deploy if you want a permanent public link!

---

## 🚀 Quick Commands Reference

### Check Your IP:
```powershell
ipconfig | findstr "IPv4"
```

### Check Servers Running:
```powershell
netstat -ano | findstr "LISTENING" | findstr ":8000 :8080"
```

### Test Local Access:
```powershell
curl http://localhost:8080 -UseBasicParsing
curl http://192.168.0.145:8080 -UseBasicParsing
```

### Add Firewall Rules:
```powershell
New-NetFirewallRule -DisplayName "IntelliVuln Frontend" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "IntelliVuln Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### Remove Firewall Rules:
```powershell
Remove-NetFirewallRule -DisplayName "IntelliVuln Frontend"
Remove-NetFirewallRule -DisplayName "IntelliVuln Backend"
```

---

## 📞 Support Message for Your Friend

Copy and send this to your friend:

```
🔐 IntelliVuln Hub - Security Scanner Demo

Hey! I'm running a security vulnerability scanner on my computer.
You can access it from your device if you're on the same Wi-Fi.

📱 Access Link:
http://192.168.0.145:8080

🌐 Requirements:
- Connect to my Wi-Fi network: [YOUR_WIFI_NAME]
- Use any browser (Chrome, Firefox, Safari, etc.)

🎯 What to Try:
1. Check out the Dashboard (main page)
2. Go to Scanner tab
3. Try scanning: scanme.nmap.org
4. Uncheck all tools except "Nmap"
5. Click "Start Scan" and watch the progress
6. Check results in Analyzer tab
7. Try the AI Security Assistant

⚠️ Note:
- This is running on my computer
- Only works while I'm running the servers
- If it doesn't load, let me know!

🛠️ Troubleshooting:
- Make sure you're on the same Wi-Fi
- Try refreshing the page
- Try http://192.168.56.1:8080 if first link doesn't work

Let me know what you think! 🚀
```

---

## ✅ Final Checklist

**For Same Network Sharing (Recommended):**
1. ✅ Run firewall configuration commands
2. ✅ Verify servers are running
3. ✅ Test on your phone first
4. ✅ Share link: http://192.168.0.145:8080
5. ✅ Keep both PowerShell windows open
6. ✅ Monitor for issues

**Current Status:**
- Your IP: **192.168.0.145**
- Frontend: **http://192.168.0.145:8080** ✅
- Backend: **http://192.168.0.145:8000** ✅
- Both servers: **RUNNING** ✅
- Network access: **CONFIGURED** ✅

**Share this link with your friend:**
```
http://192.168.0.145:8080
```

---

**Note**: This link only works while your servers are running and your friend is on the same Wi-Fi network. For internet sharing, use ngrok or deploy to cloud!
