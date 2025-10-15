# 🌐 QUICK SHARE - One Page Guide

## 📱 Links to Share with Your Friend

**If on the SAME Wi-Fi:**
```
http://192.168.0.145:8080
```

**Alternative:**
```
http://192.168.56.1:8080
```

---

## ⚡ Quick Setup (2 Steps)

### Step 1: Open Firewall Ports

Open PowerShell **AS ADMINISTRATOR** and run:

```powershell
New-NetFirewallRule -DisplayName "IntelliVuln Frontend" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow

New-NetFirewallRule -DisplayName "IntelliVuln Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

✅ Done! Firewall is now configured.

### Step 2: Share the Link

Send your friend:
```
http://192.168.0.145:8080
```

Make sure they're on the **same Wi-Fi** as you!

---

## 🧪 Test First

Before your friend tries, test on your phone:
1. Connect phone to same Wi-Fi
2. Open browser
3. Go to: `http://192.168.0.145:8080`
4. Should see the dashboard ✅

---

## ❌ Remove Access Later

When done sharing, remove firewall rules:

```powershell
Remove-NetFirewallRule -DisplayName "IntelliVuln Frontend"
Remove-NetFirewallRule -DisplayName "IntelliVuln Backend"
```

---

## 🌍 Share Over Internet (Not Same Wi-Fi)?

Use **ngrok**:

1. Download: https://ngrok.com/download
2. Run: `ngrok http 8080`
3. Share the https link it gives you

Your friend can access from anywhere!

---

## ⚠️ Requirements

✅ **Your servers must be running** (2 PowerShell windows)
✅ **Friend must be on same Wi-Fi** (or use ngrok)
✅ **Firewall ports must be open** (run commands above)

---

## 💬 Message to Send Your Friend

```
Hey! Check out my security scanner project:

🔗 http://192.168.0.145:8080

Make sure you're connected to my Wi-Fi!

Try:
- Dashboard (view stats)
- Scanner tab (scan: scanme.nmap.org)
- AI Assistant (ask security questions)

Let me know if it doesn't load!
```

---

**That's it! Simple as that.** 🚀

See SHARING_GUIDE.md for detailed instructions and troubleshooting.
