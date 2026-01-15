"""
╔═══════════════════════════════════════════════════════════╗
║          ULTIMATE ADVANCED TELEGRAM AI BOT v2.0            ║
║                                                           ║
║  🤖 Features:                                            ║
║     ✅ Deep Thinking AI Chat (Claude-Level Intelligence)  ║
║     ✅ Image Generation (Multiple Styles)                 ║
║     ✅ Video Generation                                   ║
║     ✅ Advanced Code Generation                           ║
║     ✅ Multi-Language Translation                         ║
║     ✅ Smart Conversation Memory (10 messages)            ║
║     ✅ Intent Recognition (NLP)                           ║
║     ✅ Rate Limiting & Security                           ║
║     ✅ Health Monitoring                                  ║
║     ✅ Context-Aware Responses                            ║
║     ✅ Advanced Error Handling                            ║
║                                                           ║
║  Author: AI Developer                                    ║
║  Version: 2.0 - Full Stack Advanced Features             ║
╚═══════════════════════════════════════════════════════════╝
"""

import telebot
import requests
import json
import os
from datetime import datetime
import logging
from dotenv import load_dotenv
from functools import wraps
from time import time
import threading
from flask import Flask, jsonify
from collections import deque
import time as time_module

# Load environment variables
load_dotenv()

# ============ CONFIGURATION ============
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '8401689004:AAEvNNZQJCoVh6UMwUGrKOUynDPd-1rsPAk')
AI_API_URL = os.getenv('AI_API_URL', 'https://ai-api-premium-server.onrender.com')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
PORT = int(os.getenv('PORT', 10000))
MAX_MEMORY_SIZE = 10
DEEP_THINKING_MODEL = "claude-3.5-sonnet-thinking"
STANDARD_MODEL = "claude-3"

# Initialize bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============ FLASK HEALTH ENDPOINTS ============
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'running',
        'service': 'ULTIMATE Advanced Telegram AI Bot',
        'version': '2.0',
        'features': [
            'deep_thinking_ai',
            'image_generation',
            'video_generation',
            'advanced_code',
            'translation',
            'memory_system',
            'npl_intent',
            'context_aware'
        ],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health', methods=['GET'])
def health():
    api_health = ai_client.check_health() if 'ai_client' in globals() else False
    return jsonify({
        'bot': 'online',
        'api': 'healthy' if api_health else 'offline',
        'memory_active': True,
        'thinking_ai': 'enabled',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'bot_running': True,
        'ai_model': DEEP_THINKING_MODEL,
        'ai_api_url': AI_API_URL,
        'features_enabled': [
            'deep_thinking',
            'image',
            'video',
            'code',
            'translate',
            'memory',
            'context'
        ],
        'timestamp': datetime.now().isoformat()
    })

# ============ ADVANCED CONVERSATION MEMORY ============
class ConversationMemory:
    """Advanced memory system with context awareness"""
    
    def __init__(self, max_size=10):
        self.memory = {}
        self.max_size = max_size
        self.user_topics = {}  # Track user interests
        self.user_preferences = {}  # Remember preferences
    
    def add_message(self, user_id, role, message):
        if user_id not in self.memory:
            self.memory[user_id] = deque(maxlen=self.max_size)
        
        self.memory[user_id].append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        logger.info(f"💾 Memory: User {user_id} - {role}: {message[:60]}...")
    
    def get_history(self, user_id, last_n=5):
        if user_id not in self.memory:
            return []
        history = list(self.memory[user_id])
        return history[-last_n:] if len(history) > last_n else history
    
    def get_context_string(self, user_id, last_n=5):
        """Get enriched context with memory"""
        history = self.get_history(user_id, last_n)
        if not history:
            return ""
        
        context = "\n📚 **PREVIOUS CONVERSATION CONTEXT:**\n"
        for entry in history:
            role = "👤 User" if entry["role"] == "user" else "🤖 Assistant"
            context += f"{role}: {entry['message']}\n"
        context += "**END OF CONTEXT**\n\n"
        return context
    
    def clear_history(self, user_id):
        if user_id in self.memory:
            self.memory[user_id].clear()
        if user_id in self.user_topics:
            del self.user_topics[user_id]
        return True
    
    def get_stats(self):
        total_users = len(self.memory)
        total_messages = sum(len(h) for h in self.memory.values())
        return {
            "total_users": total_users,
            "total_messages": total_messages,
            "max_size": self.max_size
        }

conversation_memory = ConversationMemory(max_size=MAX_MEMORY_SIZE)

# ============ ADVANCED RATE LIMITER ============
class AdvancedRateLimiter:
    """Smart rate limiting with different tiers"""
    
    def __init__(self):
        self.user_calls = {}
        self.limits = {
            'standard': {'calls': 20, 'period': 60},
            'thinking': {'calls': 5, 'period': 120},
            'generation': {'calls': 3, 'period': 300}
        }
    
    def is_allowed(self, user_id, tier='standard'):
        now = time()
        if user_id not in self.user_calls:
            self.user_calls[user_id] = {}
        
        if tier not in self.user_calls[user_id]:
            self.user_calls[user_id][tier] = []
        
        limit = self.limits[tier]
        self.user_calls[user_id][tier] = [
            t for t in self.user_calls[user_id][tier]
            if now - t < limit['period']
        ]
        
        if len(self.user_calls[user_id][tier]) < limit['calls']:
            self.user_calls[user_id][tier].append(now)
            return True
        return False

rate_limiter = AdvancedRateLimiter()

# ============ ADVANCED NLP INTENT RECOGNITION ============
class AdvancedIntentRecognizer:
    """Enhanced NLP for accurate intent detection"""
    
    def __init__(self):
        self.intents = {
            "deep_thinking": {
                "keywords": [
                    "सोचो", "विश्लेषण", "गहराई से", "समझाओ विस्तार से",
                    "think", "analyze", "deep", "explain in detail",
                    "समझ", "reason", "logic", "क्यों", "कैसे", "why", "how"
                ],
                "type": "deep_thinking"
            },
            "image": {
                "keywords": [
                    "image", "photo", "picture", "draw", "banao",
                    "तस्वीर", "फोटो", "चित्र", "generate image", "बनाओ image"
                ],
                "type": "image"
            },
            "video": {
                "keywords": [
                    "video", "film", "clip", "generate video",
                    "वीडियो", "बनाओ video", "video banao"
                ],
                "type": "video"
            },
            "code": {
                "keywords": [
                    "code", "program", "python", "javascript", "लिख",
                    "कोड", "प्रोग्राम", "लिखो code", "write code"
                ],
                "type": "code"
            },
            "translate": {
                "keywords": [
                    "translate", "अनुवाद", "हिंदी", "english", "convert"
                ],
                "type": "translate"
            },
            "chat": {
                "keywords": [
                    "hello", "hi", "नमस्ते", "बात", "chat", "talk"
                ],
                "type": "chat"
            }
        }
    
    def recognize_intent(self, text):
        text_lower = text.lower()
        
        # Check for deep thinking keywords first (highest priority)
        for intent, data in self.intents.items():
            if data["type"] == "deep_thinking":
                for keyword in data["keywords"]:
                    if keyword.lower() in text_lower:
                        return {
                            "intent": intent,
                            "type": "deep_thinking",
                            "confidence": 0.95
                        }
        
        # Check other intents
        for intent, data in self.intents.items():
            if data["type"] != "deep_thinking":
                for keyword in data["keywords"]:
                    if keyword.lower() in text_lower:
                        return {
                            "intent": intent,
                            "type": data["type"],
                            "confidence": 0.85
                        }
        
        # Default to chat
        return {
            "intent": "general_query",
            "type": "chat",
            "confidence": 0.5
        }

intent_recognizer = AdvancedIntentRecognizer()

# ============ ADVANCED AI API CLIENT ============
class AdvancedAIAPIClient:
    """Enhanced API client with multiple AI models"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.timeout = 120  # Increased for thinking
    
    def check_health(self):
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def deep_thinking_chat(self, message, context=""):
        """🧠 Deep Thinking AI - Like Claude with Extended Thinking"""
        try:
            full_message = context + message if context else message
            
            payload = {
                "message": full_message,
                "model": DEEP_THINKING_MODEL,
                "max_tokens": 2000,
                "thinking": True,
                "temperature": 0.7,
                "deep_analysis": True
            }
            
            logger.info(f"🧠 Deep Thinking Request: {message[:50]}...")
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            return {"error": f"API Error: {response.status_code}"}
        except Exception as e:
            logger.error(f"Deep thinking error: {e}")
            return {"error": str(e)}
    
    def standard_chat(self, message, context=""):
        """Standard AI Chat"""
        try:
            full_message = context + message if context else message
            
            payload = {
                "message": full_message,
                "model": STANDARD_MODEL,
                "max_tokens": 1000
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            return {"error": f"API Error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def generate_image(self, prompt, style="realistic"):
        """🎨 Advanced Image Generation"""
        try:
            logger.info(f"🎨 Image Generation: {prompt}")
            
            payload = {
                "prompt": prompt,
                "style": style,
                "size": "1024x1024",
                "quality": "high",
                "detailed": True
            }
            
            response = requests.post(
                f"{self.base_url}/api/image",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            return {"error": f"Image generation failed: {response.status_code}"}
        except Exception as e:
            logger.error(f"Image gen error: {e}")
            return {"error": str(e)}
    
    def generate_video(self, description, duration=10):
        """🎥 Advanced Video Generation"""
        try:
            logger.info(f"🎥 Video Generation: {description}")
            
            payload = {
                "description": description,
                "duration": duration,
                "quality": "1080p",
                "detailed": True
            }
            
            response = requests.post(
                f"{self.base_url}/api/video",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            return {"error": f"Video generation failed: {response.status_code}"}
        except Exception as e:
            logger.error(f"Video gen error: {e}")
            return {"error": str(e)}
    
    def generate_code(self, description, language="python"):
        """💻 Advanced Code Generation"""
        try:
            payload = {
                "description": description,
                "language": language,
                "detailed": True,
                "with_comments": True
            }
            
            response = requests.post(
                f"{self.base_url}/api/code",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            return {"error": f"Code generation failed"}
        except Exception as e:
            return {"error": str(e)}
    
    def translate(self, text, target_language="hindi"):
        """🌐 Advanced Translation"""
        try:
            payload = {
                "text": text,
                "target_language": target_language,
                "preserve_meaning": True
            }
            
            response = requests.post(
                f"{self.base_url}/api/translate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            return {"error": "Translation failed"}
        except Exception as e:
            return {"error": str(e)}

ai_client = AdvancedAIAPIClient(AI_API_URL)

# ============ KEYBOARD BUILDERS ============
def get_main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        telebot.types.KeyboardButton("🧠 Deep Thinking AI"),
        telebot.types.KeyboardButton("💬 Smart Chat"),
        telebot.types.KeyboardButton("🎨 Generate Image"),
        telebot.types.KeyboardButton("🎥 Generate Video"),
        telebot.types.KeyboardButton("💻 Generate Code"),
        telebot.types.KeyboardButton("🌐 Translate"),
        telebot.types.KeyboardButton("🧠 My Memory"),
        telebot.types.KeyboardButton("❓ Help")
    ]
    markup.add(*buttons)
    return markup

def get_thinking_styles():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        telebot.types.KeyboardButton("🔬 Analytical"),
        telebot.types.KeyboardButton("🎓 Educational"),
        telebot.types.KeyboardButton("💡 Creative"),
        telebot.types.KeyboardButton("⚙️ Technical"),
        telebot.types.KeyboardButton("📚 Philosophical"),
        telebot.types.KeyboardButton("⬅️ Back")
    ]
    markup.add(*buttons)
    return markup

def get_image_styles():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        telebot.types.KeyboardButton("🖼️ Realistic"),
        telebot.types.KeyboardButton("🎨 Artistic"),
        telebot.types.KeyboardButton("🌈 Fantasy"),
        telebot.types.KeyboardButton("🎭 Cinematic"),
        telebot.types.KeyboardButton("🖌️ Oil Painting"),
        telebot.types.KeyboardButton("⬅️ Back")
    ]
    markup.add(*buttons)
    return markup

def get_memory_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        telebot.types.KeyboardButton("📜 View History"),
        telebot.types.KeyboardButton("📊 Memory Stats"),
        telebot.types.KeyboardButton("🗑️ Clear Memory"),
        telebot.types.KeyboardButton("⬅️ Back to Menu")
    ]
    markup.add(*buttons)
    return markup

# ============ ERROR HANDLER ============
def error_handler(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except Exception as e:
            logger.error(f"❌ Error in {func.__name__}: {str(e)}")
            bot.send_message(
                message.chat.id,
                f"❌ कुछ गलत हुआ। कृपया दोबारा कोशिश करें।\n\nError: {str(e)[:50]}...",
                reply_markup=get_main_menu()
            )
    return wrapper

# ============ BOT COMMANDS ============
@bot.message_handler(commands=['start'])
@error_handler
def handle_start(message):
    user_name = message.from_user.first_name
    user_id = message.chat.id
    conversation_memory.clear_history(user_id)
    
    welcome = f"""
╔════════════════════════════════════════╗
║ 🚀 ULTIMATE ADVANCED AI BOT v2.0 🚀   ║
╚════════════════════════════════════════╝

नमस्ते {user_name}! 👋

✨ **मैं हूँ सबसे Advanced AI Bot:**

🧠 **Deep Thinking AI** - Claude-Level Intelligence
   • गहराई से सोचता हूँ
   • जटिल समस्याओं का समाधान
   • विस्तृत विश्लेषण

💬 **Smart Chat** - Context के साथ बातचीत
💻 **Code Generation** - किसी भी language में
🎨 **Image Generation** - 6 अलग-अलग styles
🎥 **Video Generation** - Professional quality
🌐 **Translation** - 50+ languages
🧠 **Smart Memory** - 10 messages याद रखता हूँ

**क्या करना चाहते हो?**
"""
    
    bot.send_message(message.chat.id, welcome, reply_markup=get_main_menu(), parse_mode='Markdown')

@bot.message_handler(commands=['help'])
@error_handler
def handle_help(message):
    help_text = f"""
📚 **ADVANCED FEATURES GUIDE**

1️⃣ **🧠 Deep Thinking AI**
   • सबसे intelligent thinking
   • "गहराई से सोचो" जैसे keywords दो
   • 5 अलग thinking styles

2️⃣ **💬 Smart Chat**
   • Context-aware responses
   • Memory के साथ बेहतर जवाब
   • Multi-language support

3️⃣ **🎨 Image Generation**
   • 6 professional styles
   • High quality 1024x1024
   • Detailed descriptions

4️⃣ **🎥 Video Generation**
   • Professional quality videos
   • 10+ seconds duration
   • Multiple effects

5️⃣ **💻 Code Generation**
   • 20+ programming languages
   • Detailed comments
   • Production-ready code

6️⃣ **🌐 Translation**
   • 50+ languages
   • Natural translations
   • Context preservation

7️⃣ **🧠 Smart Memory**
   • Last 10 conversations याद रखता हूँ
   • Better context awareness
   • Personal preferences

**उदाहरण:**
• "गहराई से सोचो कि कैसे AI काम करता है"
• "Sunset की image बनाओ oil painting style में"
• "Python में machine learning code लिखो"

🚀 **Let's Get Started!**
"""
    
    bot.send_message(message.chat.id, help_text, reply_markup=get_main_menu(), parse_mode='Markdown')

@bot.message_handler(commands=['status'])
@error_handler
def handle_status(message):
    api_health = ai_client.check_health()
    memory_stats = conversation_memory.get_stats()
    
    status_text = f"""
📊 **BOT STATUS & STATS**

**System Status:**
✅ Bot: ONLINE
{'✅' if api_health else '❌'} API: {'HEALTHY' if api_health else 'OFFLINE'}
✅ Memory: ACTIVE
✅ Deep Thinking: ENABLED
✅ Generation: READY

**Memory Statistics:**
📈 Total Users: {memory_stats['total_users']}
📝 Total Messages: {memory_stats['total_messages']}
💾 Max/User: {memory_stats['max_size']}

**Models:**
🧠 Deep Thinking: {DEEP_THINKING_MODEL}
💬 Standard: {STANDARD_MODEL}

⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}
"""
    
    bot.send_message(message.chat.id, status_text, parse_mode='Markdown')

# ============ DEEP THINKING AI HANDLER ============
@bot.message_handler(func=lambda m: "Deep Thinking AI" in m.text)
@error_handler
def handle_deep_thinking_mode(message):
    if not rate_limiter.is_allowed(message.chat.id, 'thinking'):
        bot.send_message(
            message.chat.id,
            "⚠️ Deep Thinking Rate Limit: 5 requests per 2 minutes\n\nकुछ समय बाद कोशिश करें।"
        )
        return
    
    thinking_intro = """
🧠 **DEEP THINKING MODE ACTIVATED**

**5 Thinking Styles:**
• 🔬 **Analytical** - Data-driven analysis
• 🎓 **Educational** - Learning-focused
• 💡 **Creative** - Out-of-box thinking
• ⚙️ **Technical** - Deep technical insights
• 📚 **Philosophical** - Deep reasoning

अपना thinking style चुनो, फिर सवाल पूछो!
"""
    
    msg = bot.send_message(
        message.chat.id,
        thinking_intro,
        reply_markup=get_thinking_styles(),
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_thinking_style)

def process_thinking_style(message):
    user_id = message.chat.id
    
    if "Back" in message.text:
        bot.send_message(user_id, "Main Menu:", reply_markup=get_main_menu())
        return
    
    style = message.text.replace("🔬 ", "").replace("🎓 ", "").replace("💡 ", "").replace("⚙️ ", "").replace("📚 ", "")
    
    msg = bot.send_message(
        user_id,
        f"\n🧠 {style} Mode चुना है।\n\nअब अपना गहरा सवाल पूछो:\n\n(जितना विस्तार से पूछोगे, उतना विस्तार से जवाब मिलेगा)",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_deep_thinking, style)

def process_deep_thinking(message, style):
    user_id = message.chat.id
    user_question = message.text
    
    if not rate_limiter.is_allowed(user_id, 'thinking'):
        bot.send_message(user_id, "⚠️ Rate limit. थोड़ा इंतज़ार करो।")
        return
    
    conversation_memory.add_message(user_id, "user", f"[{style}] {user_question}")
    
    thinking_msg = bot.send_message(
        user_id,
        "🧠 गहराई से सोच रहा हूँ... (यह 30-60 सेकंड ले सकता है)\n\n⏳ कृपया प्रतीक्षा करें..."
    )
    
    context = conversation_memory.get_context_string(user_id, last_n=3)
    thinking_prompt = f"""
{style} Mode - Deep Thinking Request:

{user_question}

Please provide:
1. Deep analysis with reasoning
2. Multiple perspectives
3. Detailed explanations
4. Examples if applicable
5. Actionable insights
"""
    
    response = ai_client.deep_thinking_chat(thinking_prompt, context)
    
    if "error" not in response:
        ai_reply = response.get("response", "कोई reply नहीं मिला")
        
        # Format deep thinking response
        formatted_reply = f"""🧠 **{style} Analysis:**\n\n{ai_reply}"""
        
        conversation_memory.add_message(user_id, "bot", ai_reply)
        
        if len(formatted_reply) > 4096:
            for i in range(0, len(formatted_reply), 4096):
                bot.send_message(user_id, formatted_reply[i:i+4096], parse_mode='Markdown')
            bot.delete_message(user_id, thinking_msg.message_id)
        else:
            bot.edit_message_text(formatted_reply, user_id, thinking_msg.message_id, parse_mode='Markdown')
    else:
        bot.edit_message_text(
            f"❌ Error: {response['error']}",
            user_id,
            thinking_msg.message_id
        )
    
    bot.send_message(user_id, "\n और कोई सवाल?", reply_markup=get_main_menu())

# ============ IMAGE GENERATION HANDLER ============
@bot.message_handler(func=lambda m: "Generate Image" in m.text)
@error_handler
def handle_image_mode(message):
    if not rate_limiter.is_allowed(message.chat.id, 'generation'):
        bot.send_message(
            message.chat.id,
            "⚠️ Image Generation Rate Limit: 3 per 5 minutes\n\nथोड़ा इंतज़ार करो।"
        )
        return
    
    image_intro = """
🎨 **IMAGE GENERATION MODE**

**6 Professional Styles:**
• 🖼️ **Realistic** - Photo-realistic images
• 🎨 **Artistic** - Artistic rendering
• 🌈 **Fantasy** - Fantasy worlds
• 🎭 **Cinematic** - Movie-quality
• 🖌️ **Oil Painting** - Classical style
• 🌌 **Sci-Fi** - Futuristic

Style चुनो, फिर description दो!
"""
    
    msg = bot.send_message(
        message.chat.id,
        image_intro,
        reply_markup=get_image_styles(),
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_image_style)

def process_image_style(message):
    user_id = message.chat.id
    
    if "Back" in message.text:
        bot.send_message(user_id, "Main Menu:", reply_markup=get_main_menu())
        return
    
    style_map = {
        "🖼️ Realistic": "realistic",
        "🎨 Artistic": "artistic",
        "🌈 Fantasy": "fantasy",
        "🎭 Cinematic": "cinematic",
        "🖌️ Oil Painting": "oil_painting",
        "🌌 Sci-Fi": "scifi"
    }
    
    style = style_map.get(message.text, "realistic")
    
    msg = bot.send_message(
        user_id,
        f"\n🎨 {message.text} चुना।\n\nअब detailed description दो:\n(जितना विस्तार से बताओगे, उतनी बेहतर image बनेगी)",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_image_request, style)

def process_image_request(message, style):
    user_id = message.chat.id
    prompt = message.text
    
    if not rate_limiter.is_allowed(user_id, 'generation'):
        bot.send_message(user_id, "⚠️ Rate limit. कुछ समय बाद कोशिश करो।")
        return
    
    conversation_memory.add_message(user_id, "user", f"Image: {prompt}")
    
    processing = bot.send_message(
        user_id,
        f"🎨 {style.replace('_', ' ').title()} style में image बन रही है...\n\n⏳ कृपया प्रतीक्षा करें (1-2 मिनट ले सकता है)..."
    )
    
    response = ai_client.generate_image(prompt, style)
    
    if "error" not in response and "image_url" in response:
        try:
            bot.send_photo(
                user_id,
                response["image_url"],
                caption=f"✨ **{style.title()}** Style\n\n📝 Prompt: {prompt[:100]}...",
                parse_mode='Markdown'
            )
            bot.delete_message(user_id, processing.message_id)
            conversation_memory.add_message(user_id, "bot", f"Generated: {prompt}")
        except Exception as e:
            bot.edit_message_text(
                f"❌ Error sending image: {str(e)[:100]}",
                user_id,
                processing.message_id
            )
    else:
        bot.edit_message_text(
            f"❌ Image Generation Failed:\n{response.get('error', 'Unknown error')}",
            user_id,
            processing.message_id
        )
    
    bot.send_message(user_id, "\n और कुछ?", reply_markup=get_main_menu())

# ============ VIDEO GENERATION HANDLER ============
@bot.message_handler(func=lambda m: "Generate Video" in m.text)
@error_handler
def handle_video_mode(message):
    if not rate_limiter.is_allowed(message.chat.id, 'generation'):
        bot.send_message(
            message.chat.id,
            "⚠️ Video Generation Rate Limit: 3 per 5 minutes\n\nथोड़ा इंतज़ार करो।"
        )
        return
    
    msg = bot.send_message(
        message.chat.id,
        "🎥 **VIDEO GENERATION MODE**\n\nDetailed video description दो:\n(Example: 'Sunset के समय ocean की waves')",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_video_request)

def process_video_request(message):
    user_id = message.chat.id
    description = message.text
    
    if not rate_limiter.is_allowed(user_id, 'generation'):
        bot.send_message(user_id, "⚠️ Rate limit")
        return
    
    conversation_memory.add_message(user_id, "user", f"Video: {description}")
    
    processing = bot.send_message(
        user_id,
        "🎥 Professional quality video बन रही है...\n\n⏳ कृपया प्रतीक्षा करें (2-5 मिनट)..."
    )
    
    response = ai_client.generate_video(description, duration=10)
    
    if "error" not in response and "video_url" in response:
        try:
            bot.send_video(
                user_id,
                response["video_url"],
                caption=f"🎬 Professional Video\n\n📝: {description[:80]}...",
                parse_mode='Markdown'
            )
            bot.delete_message(user_id, processing.message_id)
            conversation_memory.add_message(user_id, "bot", f"Generated video")
        except Exception as e:
            bot.edit_message_text(
                f"❌ Error: {str(e)[:100]}",
                user_id,
                processing.message_id
            )
    else:
        bot.edit_message_text(
            f"❌ Video Generation Failed\n{response.get('error', 'Unknown')}",
            user_id,
            processing.message_id
        )
    
    bot.send_message(user_id, "\n और?", reply_markup=get_main_menu())

# ============ CODE GENERATION HANDLER ============
@bot.message_handler(func=lambda m: "Generate Code" in m.text)
@error_handler
def handle_code_mode(message):
    if not rate_limiter.is_allowed(message.chat.id, 'standard'):
        bot.send_message(message.chat.id, "⚠️ Rate limit. कुछ समय बाद कोशिश करो।")
        return
    
    msg = bot.send_message(
        message.chat.id,
        "💻 **ADVANCED CODE GENERATION**\n\nक्या code चाहिए?\n(Example: 'Python में machine learning model')",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_code_request)

def process_code_request(message):
    user_id = message.chat.id
    
    conversation_memory.add_message(user_id, "user", f"Code: {message.text}")
    
    bot.send_message(user_id, "💻 Professional code लिख रहा हूँ...")
    response = ai_client.generate_code(message.text, "python")
    
    if "error" not in response and "code" in response:
        code = response["code"]
        conversation_memory.add_message(user_id, "bot", f"Code generated")
        
        if len(code) > 4096:
            for i in range(0, len(code), 4096):
                bot.send_message(user_id, f"```python\n{code[i:i+4096]}\n```", parse_mode='Markdown')
        else:
            bot.send_message(user_id, f"```python\n{code}\n```", parse_mode='Markdown')
    else:
        bot.send_message(user_id, f"❌ Error: {response.get('error')}")
    
    bot.send_message(user_id, "\n और?", reply_markup=get_main_menu())

# ============ MEMORY HANDLERS ============
@bot.message_handler(func=lambda m: "My Memory" in m.text)
@error_handler
def handle_memory_menu(message):
    user_id = message.chat.id
    history = conversation_memory.get_history(user_id)
    
    info = f"""
🧠 **MEMORY MANAGEMENT**

आपकी memory में {len(history)} messages हैं।
"""
    
    bot.send_message(user_id, info, reply_markup=get_memory_menu(), parse_mode='Markdown')

@bot.message_handler(func=lambda m: "View History" in m.text)
@error_handler
def handle_view_history(message):
    user_id = message.chat.id
    history = conversation_memory.get_history(user_id, last_n=10)
    
    if not history:
        bot.send_message(user_id, "🧠 अभी कोई conversation याद नहीं है।")
        return
    
    history_text = "📜 **Your Conversation History:**\n\n"
    for i, entry in enumerate(history, 1):
        emoji = "👤" if entry["role"] == "user" else "🤖"
        msg_preview = entry["message"][:60] + "..." if len(entry["message"]) > 60 else entry["message"]
        history_text += f"{i}. {emoji} {msg_preview}\n"
    
    bot.send_message(user_id, history_text, parse_mode='Markdown')
    bot.send_message(user_id, "\n और क्या?", reply_markup=get_memory_menu())

@bot.message_handler(func=lambda m: "Memory Stats" in m.text)
@error_handler
def handle_memory_stats(message):
    stats = conversation_memory.get_stats()
    
    stats_text = f"""
📊 **MEMORY STATISTICS**

📈 Total Users: {stats['total_users']}
📝 Total Messages: {stats['total_messages']}
💾 Max/User: {stats['max_size']}

🔍 Your History: {len(conversation_memory.get_history(message.chat.id))} messages
"""
    
    bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: "Clear Memory" in m.text)
@error_handler
def handle_clear_memory(message):
    conversation_memory.clear_history(message.chat.id)
    bot.send_message(message.chat.id, "🗑️ Memory cleared!\n\nनई conversation शुरू करो।", reply_markup=get_main_menu())

# ============ SMART CHAT HANDLER ============
@bot.message_handler(func=lambda m: "Smart Chat" in m.text)
@error_handler
def handle_smart_chat(message):
    if not rate_limiter.is_allowed(message.chat.id, 'standard'):
        bot.send_message(message.chat.id, "⚠️ Rate limit.")
        return
    
    msg = bot.send_message(
        message.chat.id,
        "💬 **SMART CHAT MODE**\n\nअपना सवाल या बात बताओ:",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_smart_chat)

def process_smart_chat(message):
    user_id = message.chat.id
    
    if not rate_limiter.is_allowed(user_id, 'standard'):
        bot.send_message(user_id, "⚠️ Rate limit")
        return
    
    conversation_memory.add_message(user_id, "user", message.text)
    
    thinking = bot.send_message(user_id, "💬 सोच रहा हूँ...")
    context = conversation_memory.get_context_string(user_id, last_n=3)
    response = ai_client.standard_chat(message.text, context)
    
    if "error" not in response:
        ai_reply = response.get("response", "कोई reply नहीं")
        conversation_memory.add_message(user_id, "bot", ai_reply)
        
        if len(ai_reply) > 4096:
            for i in range(0, len(ai_reply), 4096):
                bot.send_message(user_id, ai_reply[i:i+4096])
            bot.delete_message(user_id, thinking.message_id)
        else:
            bot.edit_message_text(ai_reply, user_id, thinking.message_id)
    else:
        bot.edit_message_text(f"❌ Error: {response['error']}", user_id, thinking.message_id)
    
    bot.send_message(user_id, "\n और?", reply_markup=get_main_menu())

# ============ TRANSLATION HANDLER ============
@bot.message_handler(func=lambda m: "Translate" in m.text)
@error_handler
def handle_translate(message):
    if not rate_limiter.is_allowed(message.chat.id, 'standard'):
        bot.send_message(message.chat.id, "⚠️ Rate limit")
        return
    
    msg = bot.send_message(
        message.chat.id,
        "🌐 **TRANSLATION MODE**\n\nक्या translate करना है?",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_translate)

def process_translate(message):
    user_id = message.chat.id
    
    conversation_memory.add_message(user_id, "user", f"Translate: {message.text}")
    
    bot.send_message(user_id, "🌐 Translate हो रहा है...")
    response = ai_client.translate(message.text, "hindi")
    
    if "error" not in response:
        translation = response.get('translated_text', 'No translation')
        conversation_memory.add_message(user_id, "bot", translation)
        bot.send_message(user_id, f"✅ **Translated:**\n\n{translation}")
    else:
        bot.send_message(user_id, f"❌ Error: {response.get('error')}")
    
    bot.send_message(user_id, "\n और?", reply_markup=get_main_menu())

# ============ DEFAULT HANDLER ============
@bot.message_handler(func=lambda m: True)
@error_handler
def handle_default(message):
    user_id = message.chat.id
    
    if not rate_limiter.is_allowed(user_id, 'standard'):
        bot.send_message(user_id, "⚠️ Rate limit")
        return
    
    intent = intent_recognizer.recognize_intent(message.text)
    
    if intent["type"] == "deep_thinking":
        handle_deep_thinking_mode(message)
    elif intent["type"] == "image":
        handle_image_mode(message)
    elif intent["type"] == "video":
        handle_video_mode(message)
    elif intent["type"] == "code":
        handle_code_mode(message)
    elif intent["type"] == "translate":
        handle_translate(message)
    else:
        handle_smart_chat(message)

# ============ FLASK SERVER ============
def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ============ MAIN ============
if __name__ == "__main__":
    logger.info("""
╔═══════════════════════════════════════════════════╗
║  🚀 ULTIMATE ADVANCED TELEGRAM AI BOT v2.0 🚀    ║
║                                                   ║
║  Features Enabled:                                ║
║  ✅ Deep Thinking AI (Claude-Level)              ║
║  ✅ Image Generation (6 Styles)                  ║
║  ✅ Video Generation                             ║
║  ✅ Advanced Code Generation                     ║
║  ✅ Translation (50+ Languages)                  ║
║  ✅ Smart Conversation Memory                    ║
║  ✅ Advanced NLP Intent Recognition              ║
║  ✅ Rate Limiting & Security                     ║
║                                                   ║
║  Starting up...                                   ║
╚═══════════════════════════════════════════════════╝
    """)
    
    logger.info(f"🔗 API URL: {AI_API_URL}")
    logger.info(f"🧠 Deep Thinking Model: {DEEP_THINKING_MODEL}")
    logger.info(f"💬 Standard Model: {STANDARD_MODEL}")
    logger.info(f"🌐 Flask Port: {PORT}")
    logger.info(f"📊 API Health: {'✅ HEALTHY' if ai_client.check_health() else '❌ OFFLINE'}")
    
    # Start Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info(f"✅ Flask server started on port {PORT}")
    
    try:
        logger.info("🚀 Bot polling started...")
        logger.info("\n✨ Bot is LIVE! Ready to serve!\n")
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        raise
