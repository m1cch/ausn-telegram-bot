# 🚀 Deploy to Render - Step by Step

Complete guide to deploy your AUSN Telegram bot to Render.com for **FREE 24/7 hosting**.

---

## 📋 Prerequisites

- GitHub account
- Render account (sign up at [render.com](https://render.com))
- Your Telegram bot token: `8582141259:AAGYjXmur00TkzS9WcXFpq-xnlPPVmdhe7g`

---

## 🎯 Step 1: Push Code to GitHub

### 1.1 Initialize Git (if not done)
```bash
cd "/Users/m1cch/power m2 code/ipoteka calculator"
git init
```

### 1.2 Create repository on GitHub
1. Go to [github.com](https://github.com)
2. Click **"New repository"**
3. Name: `ausn-telegram-bot`
4. Set to **Private** (recommended - your token might be in history)
5. Click **"Create repository"**

### 1.3 Push your code
```bash
# Add files
git add .

# Commit
git commit -m "Initial commit: AUSN Telegram bot"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ausn-telegram-bot.git

# Push
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Deploy on Render

### 2.1 Create Render Account
1. Go to [render.com](https://render.com)
2. Click **"Get Started"**
3. Sign up with GitHub (recommended)

### 2.2 Create New Background Worker

1. **Dashboard** → Click **"New +"** → Select **"Background Worker"**

2. **Connect Repository:**
   - Click **"Connect GitHub"**
   - Find and select your `ausn-telegram-bot` repository
   - Click **"Connect"**

3. **Configure Service:**
   ```
   Name: ausn-telegram-bot
   Region: Choose closest to you (e.g., Frankfurt for Europe)
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python bot.py
   ```

4. **Select Plan:**
   - Choose **"Free"** plan
   - Free tier includes:
     - ✅ 750 hours/month (enough for 24/7)
     - ✅ Automatic deploys
     - ✅ HTTPS
     - ⚠️ May spin down after 15 min inactivity (spins up on new message)

5. **Environment Variables:**
   - Click **"Add Environment Variable"**
   - Add:
     ```
     Key: TELEGRAM_BOT_TOKEN
     Value: 8582141259:AAGYjXmur00TkzS9WcXFpq-xnlPPVmdhe7g
     ```
   - ⚠️ **IMPORTANT:** Never commit this to Git!

6. **Create Service:**
   - Click **"Create Background Worker"**
   - Wait 2-3 minutes for deployment

### 2.3 Check Status
- Your bot should show **"Deploy succeeded"** and **"Live"** status
- Check logs for: `INFO - Бот запущен...`

---

## ✅ Step 3: Test Your Bot

1. Open your bot in Telegram
2. Send `/start`
3. Enter test data:
   - Income: `2000000`
   - Expenses: `800000`
4. Should receive calculation results! 🎉

---

## 📊 Monitor Your Bot

### View Logs
1. Go to Render Dashboard
2. Click on your service
3. Click **"Logs"** tab
4. See real-time bot activity

### Check Metrics
- **Metrics** tab shows:
  - Memory usage
  - CPU usage
  - Restart count

---

## 🔄 Update Your Bot

### Method 1: Auto-deploy (Recommended)
1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update bot features"
   git push
   ```
3. Render automatically detects changes and redeploys! ✅

### Method 2: Manual Deploy
1. Go to Render Dashboard
2. Click on your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🛠 Troubleshooting

### Bot Not Starting?

**Check logs for errors:**
```
Dashboard → Your Service → Logs
```

**Common issues:**

1. **"TELEGRAM_BOT_TOKEN not found"**
   - Solution: Add environment variable in Render settings

2. **"Invalid token"**
   - Solution: Check token is correct (no spaces, complete)
   - Get new token: `/token` in [@BotFather](https://t.me/BotFather)

3. **"ModuleNotFoundError"**
   - Solution: Check `requirements.txt` is committed
   - Verify build command: `pip install -r requirements.txt`

4. **"No module named 'telegram'"**
   - Solution: Update requirements.txt versions

### Bot Stops Responding?

**Free tier limitations:**
- Spins down after 15 min of inactivity
- Wakes up automatically on new Telegram message
- First message after sleep may take 30-60 seconds

**Solution for 24/7:**
- Upgrade to paid plan ($7/month)
- Or: Use cron-job.org to ping your bot every 10 minutes

---

## 🎯 Alternative: One-Click Deploy

You can also use Render's one-click deploy:

1. Add this button to your README.md:
```markdown
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
```

2. Render will read `render.yaml` and auto-configure everything!

---

## 💰 Pricing

### Free Tier ✅
- 750 hours/month (24/7 for 1 service)
- Automatic SSL
- Auto-deploys from GitHub
- ⚠️ Spins down after inactivity

### Paid Tier ($7/month)
- No spin down
- More resources
- Better performance
- Priority support

---

## 🔒 Security Best Practices

1. ✅ **Never commit `.env` file**
   ```bash
   # Already in .gitignore
   echo ".env" >> .gitignore
   ```

2. ✅ **Use Render Environment Variables**
   - Not in code
   - Not in Git history
   - Encrypted at rest

3. ✅ **Keep repository private** (if possible)

4. ⚠️ **If token leaked:**
   - Revoke immediately: [@BotFather](https://t.me/BotFather) → `/mybots` → Bot Settings → Revoke Token
   - Generate new token
   - Update in Render environment variables

---

## 📚 Useful Render Commands

### View Recent Logs
```bash
# Install Render CLI
npm install -g render

# Login
render login

# View logs
render logs -s your-service-name
```

### Restart Service
Dashboard → Your Service → Manual Deploy → "Clear build cache & deploy"

---

## 🎉 Success!

Your bot is now:
- ✅ Running 24/7 on Render
- ✅ Automatically deploying from GitHub
- ✅ Secure (token in environment variables)
- ✅ Free (on free tier)
- ✅ Scalable (upgrade when needed)

**Bot URL in Telegram:**
Find via [@BotFather](https://t.me/BotFather) → `/mybots`

---

## 🆘 Need Help?

- **Render Docs:** [render.com/docs](https://render.com/docs)
- **Render Support:** [render.com/support](https://render.com/support)
- **Telegram Bot API:** [core.telegram.org/bots](https://core.telegram.org/bots)

---

## 📝 Quick Commands Summary

```bash
# Push to GitHub
git add .
git commit -m "Your message"
git push

# Render automatically deploys on push!

# Check status
curl https://api.render.com/v1/services

# View logs in browser
# https://dashboard.render.com → Your Service → Logs
```

---

**🚀 Your bot is live! Start using it now!**

