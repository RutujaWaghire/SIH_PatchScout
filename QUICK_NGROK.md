# 🌍 SHARE OVER INTERNET - Quick Guide

## Your friend is NOT on same Wi-Fi? Use ngrok!

---

## ⚡ 3-Minute Setup

### 1️⃣ Download ngrok
https://ngrok.com/download
- Download for Windows
- Extract to `C:\ngrok\`

### 2️⃣ Get Your Token
https://dashboard.ngrok.com/signup
- Sign up (free)
- Copy your authtoken from dashboard

### 3️⃣ Configure
```powershell
cd C:\ngrok
.\ngrok.exe config add-authtoken YOUR_TOKEN_HERE
```

### 4️⃣ Start Tunnel
```powershell
cd C:\ngrok
.\ngrok.exe http 8080
```

### 5️⃣ Share the Link!
Copy the `https://xyz.ngrok-free.app` URL and send to your friend!

---

## 📱 What to Send Your Friend

```
Hey! Check out my project:
https://abc123xyz.ngrok-free.app
(Your actual ngrok URL here)

Works from anywhere! 🌍
```

---

## ✅ Requirements

- ✅ Keep your 2 server terminals running
- ✅ Keep ngrok terminal open (3rd terminal)
- ✅ Don't close any terminals while sharing

---

## 📺 What You'll See

```
ngrok

Forwarding    https://abc123xyz.ngrok-free.app -> http://localhost:8080
```

**↑ This is the link to share!**

---

## ⏹️ Stop Sharing

Press `Ctrl+C` in ngrok terminal

---

**See NGROK_SETUP.md for detailed instructions!**
