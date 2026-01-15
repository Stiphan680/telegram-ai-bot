# 🚀 Quick Start Guide - 5 Minutes Me Bot Chalao!

## 💯 Yeh Bot Kya Karega?

```
💬 "Namaste! Tum kaun ho?" ➜ Bot replies
🎨 "Ek sunset ki image banao" ➜ AI generates image
💻 "Python me fibonacci likho" ➜ Code generation
🌐 "Hello ko hindi me translate karo" ➜ Translation
📊 "100, 200, 150, 300 ka analysis karo" ➜ Data analysis
```

---

## 🔚 Pre-requisites

✅ Python 3.8+ installed
✅ pip installed
✅ Telegram account (free)
✅ Internet connection
✅ Telegram Token (neeche setup hai)

---

## ⏳ Step 1: Setup (2 Minutes)

### Option A: Windows/Mac (Easiest)

1. **Download Code**
   ```bash
   git clone https://github.com/Stiphan680/telegram-ai-bot.git
   cd telegram-ai-bot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Configuration**
   ```bash
   # .env file banao
   echo TELEGRAM_TOKEN="8401689004:AAEvNNZQJCoVh6UMwUGrKOUynDPd-1rsPAk" > .env
   echo AI_API_URL="https://ai-api-premium-server.onrender.com" >> .env
   ```

4. **Run Bot**
   ```bash
   python bot.py
   ```

   ✅ Success! Output dekhoge:
   ```
   Bot started successfully!
   API Health: True
   polling...
   ```

---

## 📱 Step 2: Telegram Pe Bot Find Karo

1. **Telegram app kholo** (or @BotFather)
2. **Search karo:** @BotFather
3. **/start** type karo
4. **/newbot** command do
5. Bot ka name enter karo (e.g., "MyAIBot")
6. Unique username dedo (e.g., "My_AI_Bot_123")
7. Token copy karo (wo upar wala token replace kar sakta hai)

**Ya seedha yeh bot ko message kar:**

Bot telegram pe available hone ke baad, usko search karo ya yeh link use karo:
```
https://t.me/8401689004:AAEvNNZQJCoVh6UMwUGrKOUynDPd-1rsPAk
```

---

## 🤫 Step 3: Bot Use Karo!

### Main Commands

```
/start    - Bot ko start karo
/help     - Help message dekhao
/health   - API status check karo
```

### Main Features

**1️⃣ Chat with AI**
```
User: "Python me lambda functions kya hote hain?"
Bot:  "Lambda functions anonymous functions hote hain..."
```

**2️⃣ Generate Image**
```
User: "Ek mountain sunset ki image banao"
Bot:  [Beautiful sunset image]
```

**3️⃣ Generate Code**
```
User: "Python me factorial function likho"
Bot:  
"""
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
"""
```

**4️⃣ Translate**
```
User: "'Good Morning' ko hindi me translate karo"
Bot:  "Shubh Prabhaat"
```

**5️⃣ Analyze Data**
```
User: "100, 200, 150, 300, 250 ka analysis karo"
Bot:  "Average: 200, Min: 100, Max: 300"
```

---

## 🔍 Troubleshooting

### Bot Respond Nahi Kar Raha?

**Fix 1: Token Check Karo**
```bash
# .env file ko check karo
cat .env
# Output: TELEGRAM_TOKEN=...
```

**Fix 2: API Connection Test Karo**
```python
import requests
response = requests.get("https://ai-api-premium-server.onrender.com/health")
print(response.status_code)  # 200 hona chahiye
```

**Fix 3: Logs Dekhao**
```bash
# Terminal mein error messages dekho
python bot.py  # Ctrl+C se stop karo
```

### Bot Slow Chal Raha Hai?

- API kuch samay le sakta hai
- Wait 30 seconds
- Network connection check karo

### "ImportError: No module named 'telebot'"

```bash
# Dependencies install karo
pip install -r requirements.txt
```

---

## 🔧 Advanced Setup (Optional)

### Render Pe Deploy Karo (Free Hosting)

1. **[Render.com](https://render.com) pe account banao**
2. **GitHub se GitHub repository connect karo**
3. **New "Web Service" create karo**
4. **Environment variables set karo:**
   ```
   TELEGRAM_TOKEN = "8401689004:AAEvNNZQJCoVh6UMwUGrKOUynDPd-1rsPAk"
   AI_API_URL = "https://ai-api-premium-server.onrender.com"
   ```
5. **Deploy karo!**

✅ Bot 24/7 chalta rahega!

---

## 🔐 Security Tips

```bash
# ❌ NEVER karo
TELEGRAM_TOKEN="token_here"

# ✅ YEH karo
export TELEGRAM_TOKEN="token_here"
# ya .env file mein
```

```bash
# .gitignore mein add karo
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

---

## 📚 Useful Links

- **GitHub Repo:** [telegram-ai-bot](https://github.com/Stiphan680/telegram-ai-bot)
- **Telegram BotFather:** @BotFather
- **AI API:** [ai-api-premium-server.onrender.com](https://ai-api-premium-server.onrender.com)
- **pyTelegramBotAPI:** [GitHub](https://github.com/eternnoir/pyTelegramBotAPI)

---

## 🙋 Help Chahiye?

### Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| Bot offline | Check render.com dashboard |
| No replies | Verify TELEGRAM_TOKEN |
| API errors | Check AI_API_URL |
| Slow responses | API loading hai, 30s wait karo |
| Random crashes | Check logs, restart bot |

---

## 🚀 Next Steps

1. **Bot Customize Karo** - Keywords change karo bot.py mein
2. **Database Add Karo** - User data save karne ke liye
3. **Webhooks Setup Karo** - Faster than polling
4. **Admin Commands Add Karo** - Control ke liye
5. **Analytics Add Karo** - Usage tracking ke liye

---

**Congratulations! 🎉 Bot setup ho gaya hai!**

*Happy Coding! 🙋*
