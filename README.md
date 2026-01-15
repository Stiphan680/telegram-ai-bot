# 🤖 Advanced Telegram AI Bot

**एक Advanced AI-powered Telegram Bot जो NLP से user intent समझता है और interactive buttons provide करता है।**

## ✨ Features

### 🎯 **Smart Intent Recognition**
- **NLP-based** user intent detection
- User के message से automatically समझ जाता है कि क्या चाहिए
- Hindi और English दोनों में काम करता है
- Confidence scores के साथ intent detection

### 💬 **AI Chat Mode**
- Claude 3, GPT-4, GPT-3.5 models support
- Multi-turn conversations
- Context-aware responses
- लंबे responses को automatically handle करता है

### 🎨 **Image Generation**
- Multiple styles:
  - 🎨 Realistic
  - 🌈 Artistic
  - 🎮 3D Render
  - ✨ Fantasy
- 1024x1024 resolution
- DALL-E, Midjourney style outputs

### 💻 **Code Generation**
- Multiple programming languages:
  - 🐍 Python
  - 📚 JavaScript
  - ☕ Java
  - 🦀 Rust
  - और बहुत कुछ...
- Production-ready code snippets
- Comments के साथ well-documented code

### 🌐 **Translation**
- 50+ languages support
- High accuracy translations
- Hindi ↔ English primary focus

### 📊 **Data Analysis**
- Raw data से meaningful insights
- Statistical analysis
- Trend detection

### 🎛️ **Interactive Buttons**
- **Reply Keyboard Buttons** - Main menu के लिए
- **Inline Buttons** - Image styles, code languages के लिए
- Smooth user experience
- Context-aware button suggestions

---

## 🚀 Setup Guide

### Prerequisites
```bash
# Python 3.8 या newer
python --version

# pip installed होना चाहिए
pip --version
```

### Step 1: Clone Repository
```bash
git clone https://github.com/Stiphan680/telegram-ai-bot.git
cd telegram-ai-bot
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configuration

#### Option A: Direct Configuration (Development)
```python
# bot.py में ये values set करो:
TELEGRAM_TOKEN = "8401689004:AAEvNNZQJCoVh6UMwUGrKOUynDPd-1rsPAk"
AI_API_URL = "https://ai-api-premium-server.onrender.com"
```

#### Option B: Environment Variables (Production) ✅ Recommended
```bash
# .env file बनाओ
echo "TELEGRAM_TOKEN=8401689004:AAEvNNZQJCoVh6UMwUGrKOUynDPd-1rsPAk" > .env
echo "AI_API_URL=https://ai-api-premium-server.onrender.com" >> .env
```

फिर bot.py में:
```python
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
AI_API_URL = os.getenv('AI_API_URL')
```

### Step 4: Run Bot
```bash
# Local में run करने के लिए
python bot.py

# या production के लिए (with gunicorn)
gunicorn bot:app
```

---

## 📱 Bot Usage

### Start Bot
```
/start - Bot को start करो और main menu देखो
/help - सभी features की information
```

### Main Menu Options

#### 1️⃣ **💬 Chat with AI**
- किसी भी topic पर बातचीत करो
- Multiple chat modes:
  - Quick Chat - तेजी से replies
  - Focused Question - detailed answers
  - Brainstorm - creative ideas

**Examples:**
```
"Python में decorators कैसे काम करते हैं?"
"Machine Learning क्या है?"
"मुझे एक अच्छा startup idea दो"
```

#### 2️⃣ **🎨 Generate Image**
- अपनी सोच का image बनवाओ
- Style select करो (Realistic, Artistic, 3D, Fantasy)

**Examples:**
```
"एक सुंदर mountain sunset की image बनाओ"
"Cyberpunk city का image generate करो"
"एक cartoon style की image चाहिए"
```

#### 3️⃣ **💻 Generate Code**
- किसी भी language में code लिखवाओ
- Production-ready snippets

**Examples:**
```
"Python में fibonacci function लिख दो"
"JavaScript में todo list app का code दो"
"Factorial calculator Java में बनाओ"
```

#### 4️⃣ **🌐 Translate**
- 50+ languages में translation
- Accurate और natural translations

**Examples:**
```
"Hello को Hindi में translate करो"
"'Good morning' को Spanish में convert करो"
```

#### 5️⃣ **📊 Analyze Data**
- Raw data से insights
- Statistical analysis

**Examples:**
```
"100, 200, 150, 300, 250 का analysis करो"
"इन sales numbers में trend क्या है?"
```

#### 6️⃣ **❓ Help**
- सभी features की detailed information
- Usage examples

---

## 🧠 NLP Intent Recognition System

Bot automatically समझ जाता है कि user क्या करना चाहता है:

### Intent Detection
```python
Intents:
├── greeting - "hello", "hi", "namaste"
├── help - "help", "sahayata", "features"
├── chat - "baat karo", "conversation"
├── image - "image", "picture", "tasveer"
├── code - "code", "program", "likho"
├── translate - "translate", "anuvaad"
└── analyze - "analyze", "data analysis"
```

### Confidence Scores
- 0.85+ - High confidence matching
- 0.50-0.85 - General query (fallback to chat)
- < 0.50 - Default chat mode

---

## ⚙️ API Integration

### Supported Endpoints

```
🏥 GET /health - API health check
💬 POST /api/chat - AI Chat
🎨 POST /api/image - Image Generation
💻 POST /api/code - Code Generation
🌐 POST /api/translate - Translation
📊 POST /api/analyze - Data Analysis
📹 POST /api/video - Video Generation
```

### Chat Request Example
```python
payload = {
    "message": "Python में async/await कैसे काम करता है?",
    "model": "claude-3",
    "max_tokens": 500
}
response = requests.post(
    "https://ai-api-premium-server.onrender.com/api/chat",
    json=payload
)
```

### Image Request Example
```python
payload = {
    "prompt": "एक नीले रंग की Ferrari",
    "style": "realistic",
    "size": "1024x1024"
}
response = requests.post(
    "https://ai-api-premium-server.onrender.com/api/image",
    json=payload
)
```

---

## 🔧 Advanced Features

### 1. Context Awareness
- Previous messages को remember करता है
- Multi-turn conversations support
- User preferences को track करता है

### 2. Error Handling
```python
# Graceful error handling
- API timeouts handle करता है
- Network errors के लिए retry logic
- User-friendly error messages
```

### 3. Response Processing
```python
# Long responses को handle करता है
- 4096 character limit को split करता है
- Proper formatting maintain करता है
- Code blocks को preserve करता है
```

### 4. Button Management
```python
# Multiple button types
ReplyKeyboardMarkup - Main menu (persistent)
InlineKeyboardMarkup - Options (temporary)
CallbackQuery - Button action handling
```

---

## 📊 Bot Architecture

```
┌─────────────────────────────────────┐
│     Telegram User Messages          │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│   Intent Recognition System (NLP)   │
│   - Keyword matching                │
│   - Confidence scoring              │
│   - Multi-language support          │
└────────────────┬────────────────────┘
                 │
     ┌───────────┼───────────┐
     │           │           │
     ▼           ▼           ▼
 ┌────────┐ ┌────────┐ ┌────────┐
 │ Chat   │ │ Image  │ │ Code   │
 │Handler │ │Handler │ │Handler │
 └────┬───┘ └────┬───┘ └────┬───┘
      │         │         │
      └────────┬┴────────┬─┘
               │
               ▼
    ┌──────────────────────┐
    │  AI API Integration  │
    │ (Render Deployed)    │
    └─────────┬────────────┘
              │
              ▼
    ┌──────────────────────┐
    │  Response Processing │
    │  & Button Rendering  │
    └─────────┬────────────┘
              │
              ▼
    ┌──────────────────────┐
    │  Telegram User       │
    │  (Response Display)  │
    └──────────────────────┘
```

---

## 🚀 Deployment Options

### Option 1: Local Server
```bash
python bot.py
```

### Option 2: Render (Free Tier) ✅ Recommended
1. [Render.com](https://render.com) पर account बनाओ
2. नया Web Service create करो
3. GitHub repository को connect करो
4. Environment variables set करो
5. Deploy करो

### Option 3: Heroku
```bash
heroku create your-bot-name
heroku config:set TELEGRAM_TOKEN="your_token"
heroku config:set AI_API_URL="your_api_url"
git push heroku main
```

### Option 4: AWS Lambda + API Gateway
- Serverless architecture
- Auto-scaling
- Pay-as-you-go pricing

---

## 🔐 Security Best Practices

### 1. Token Management
```bash
# ❌ NEVER करो
TELEGRAM_TOKEN = "8401689004:AAEvNNZQJCoVh6UMwUGrKOUynDPd-1rsPAk"  # Direct in code

# ✅ करो
export TELEGRAM_TOKEN="8401689004:AAEvNNZQJCoVh6UMwUGrKOUynDPd-1rsPAk"
# या .env file में
```

### 2. API Rate Limiting
```python
import time
from functools import wraps

def rate_limit(calls=10, period=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Rate limit logic
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### 3. Input Validation
```python
def validate_input(text):
    if len(text) > 5000:
        return False
    if "<script>" in text.lower():
        return False
    return True
```

### 4. CORS Security
- API केवल authorized endpoints से ही accept करता है
- HTTPS connections mandatory

---

## 📝 Configuration Examples

### Custom Intent Keywords (bot.py में modify करो)
```python
self.intents["greeting"]["keywords"].extend(["अरे", "वाह", "खैर"])
self.intents["chat"]["keywords"].extend(["बताओ", "समझाओ", "क्या है"])
```

### API Timeout Setting
```python
self.timeout = 30  # seconds
```

### Maximum Token Limit
```python
"max_tokens": 1000  # Increase for longer responses
```

---

## 🐛 Troubleshooting

### Bot doesn't respond
```bash
# Check token
echo $TELEGRAM_TOKEN

# Test API connection
curl https://api.telegram.org/bot{TOKEN}/getMe

# Check logs
python bot.py  # Run in foreground to see errors
```

### API connection errors
```python
# Check API health
response = ai_client.check_health()
if response:
    print("API is healthy")
else:
    print("API connection failed")
```

### Message not sending
- Chat ID verify करो
- Token की validity check करो
- API rate limits check करो

---

## 📚 Resources

- [Telegram Bot API Docs](https://core.telegram.org/bots/api)
- [pyTelegramBotAPI Documentation](https://github.com/eternnoir/pyTelegramBotAPI)
- [AI API Documentation](https://ai-api-premium-server.onrender.com)
- [NLP Concepts](https://www.coursera.org/courses?query=nlp)

---

## 📞 Support

### Issues आने पर:
1. GitHub Issues में report करो
2. Error logs share करो
3. Configuration details share करो (sensitive data छोड़ कर)

---

## 📄 License

MIT License - Free to use and modify

---

## 🙏 Credits

- pyTelegramBotAPI - Bot framework
- Render - API hosting
- OpenAI - AI models
- Anthropic - Claude models

---

**Happy Botting! 🚀**

*Last Updated: January 15, 2026*
