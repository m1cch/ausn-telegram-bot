# ⚡ Deploy to Render RIGHT NOW - 5 Minutes

## 🎯 Quick Start (Copy-Paste Commands)

### Step 1: Push to GitHub (2 min)

```bash
# Navigate to project
cd "/Users/m1cch/power m2 code/ipoteka calculator"

# Initialize Git
git init
git add .
git commit -m "Initial commit: AUSN bot"

# Create repo on GitHub, then:
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/ausn-telegram-bot.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render (3 min)

1. **Go to:** [render.com](https://render.com) → Sign up with GitHub

2. **Click:** New + → Background Worker

3. **Connect:** Your `ausn-telegram-bot` repository

4. **Configure:**
   - Name: `ausn-telegram-bot`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
   - Plan: **Free**

5. **Add Environment Variable:**
   ```
   TELEGRAM_BOT_TOKEN = 8582141259:AAGYjXmur00TkzS9WcXFpq-xnlPPVmdhe7g
   ```

6. **Click:** "Create Background Worker"

7. **Wait 2-3 minutes** for deployment ✅

---

## ✅ Done!

Your bot is now **live 24/7** on Render!

Test: Open bot in Telegram → `/start` → Enter income/expenses → Get results! 🎉

---

## 🔄 Update Bot Later

```bash
# Make changes, then:
git add .
git commit -m "Update features"
git push

# Render auto-deploys! ✅
```

---

## 📊 Check Status

**Dashboard:** [dashboard.render.com](https://dashboard.render.com)
- View logs
- Check status
- Monitor usage

---

## ⚠️ Important

- ✅ `.env` is in `.gitignore` (your token is safe)
- ✅ Add token only in Render dashboard
- ✅ Never commit tokens to GitHub
- ⚠️ If token leaked → revoke via [@BotFather](https://t.me/BotFather)

---

**🚀 Full guide:** See `RENDER_DEPLOY.md` for detailed instructions.

