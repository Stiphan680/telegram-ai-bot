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
                f"❌ कुछ गलत हुआ। कृपया दोबारा कोशिश करें।\n\nError: {str(e)[:50]}..."
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
💬 **Smart Chat** - Context के साथ बातचीत
💻 **Code Generation** - किसी भी language में
🎨 **Image Generation** - Multiple styles
🎥 **Video Generation** - Professional quality
🌐 **Translation** - 50+ languages
🧠 **Smart Memory** - 10 messages याद रखता हूँ

👉 बस normal message bhejo, main **intent detect karke** सही feature use करूँगा.
"""
    
    bot.send_message(message.chat.id, welcome, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
@error_handler
def handle_help(message):
    help_text = """📚 **HOW TO USE (Buttons हट गए, pure smart mode):**

बस normal language mein message bhejo, bot khud decide karega:

- Agar tum likho: "गहराई से समझाओ", "why", "how" → 🧠 Deep Thinking AI
- Agar tum likho: "image", "photo", "तस्वीर" → 🎨 Image Generation
- Agar tum likho: "video", "वीडियो" → 🎥 Video Generation
- Agar tum likho: "code", "python", "program" → 💻 Code Generation
- Agar tum likho: "translate", "अनुवाद" → 🌐 Translation
- Baaki sab normal chat → 💬 Smart Chat

Example messages:
- "गहराई से सोचो AI ka future kya hoga"
- "Mountain par sunset ki realistic image banao"
- "Python mein login system ka code likho"
- "Isko Hindi mein translate karo: I love programming"
"""
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
@error_handler
def handle_status(message):
    api_health = ai_client.check_health()
    memory_stats = conversation_memory.get_stats()
    
    status_text = f"""📊 **BOT STATUS & STATS**

Bot: ✅ ONLINE
API: {'✅ HEALTHY' if api_health else '❌ OFFLINE'}
Memory: 🧠 ACTIVE

Users with memory: {memory_stats['total_users']}
Total messages stored: {memory_stats['total_messages']}
Max messages per user: {memory_stats['max_size']}
"""
    bot.send_message(message.chat.id, status_text, parse_mode='Markdown')

# ============ FEATURE HANDLERS (NO BUTTON FLOWS) ============

def run_deep_thinking(user_id, user_text):
    if not rate_limiter.is_allowed(user_id, 'thinking'):
        bot.send_message(user_id, "⚠️ Deep Thinking limit cross ho gaya, thoda wait karo.")
        return
    
    conversation_memory.add_message(user_id, "user", user_text)
    thinking_msg = bot.send_message(user_id, "🧠 गहराई से सोच रहा हूँ... (30-60 sec लग सकते हैं)")
    context = conversation_memory.get_context_string(user_id, last_n=3)
    
    response = ai_client.deep_thinking_chat(user_text, context)
    if "error" not in response:
        ai_reply = response.get("response", "कोई reply नहीं मिला")
        conversation_memory.add_message(user_id, "bot", ai_reply)
        final_text = f"🧠 **Deep Thinking Result:**\n\n{ai_reply}"
        if len(final_text) > 4096:
            for i in range(0, len(final_text), 4096):
                bot.send_message(user_id, final_text[i:i+4096], parse_mode='Markdown')
            bot.delete_message(user_id, thinking_msg.message_id)
        else:
            bot.edit_message_text(final_text, user_id, thinking_msg.message_id, parse_mode='Markdown')
    else:
        bot.edit_message_text(f"❌ Error: {response['error']}", user_id, thinking_msg.message_id)


def run_image_generation(user_id, user_text):
    if not rate_limiter.is_allowed(user_id, 'generation'):
        bot.send_message(user_id, "⚠️ Image generation limit cross ho gaya, thoda wait karo.")
        return
    
    conversation_memory.add_message(user_id, "user", f"Image: {user_text}")
    processing = bot.send_message(user_id, "🎨 Image ban rahi hai... 30-90 sec wait karo...")
    response = ai_client.generate_image(user_text, style="realistic")
    
    if "error" not in response and "image_url" in response:
        try:
            bot.send_photo(user_id, response["image_url"], caption=f"🖼️ {user_text[:80]}...", parse_mode='Markdown')
            bot.delete_message(user_id, processing.message_id)
            conversation_memory.add_message(user_id, "bot", f"Image generated")
        except Exception as e:
            bot.edit_message_text(f"❌ Send error: {str(e)[:80]}", user_id, processing.message_id)
    else:
        bot.edit_message_text(f"❌ Image generation failed: {response.get('error', 'Unknown error')}", user_id, processing.message_id)


def run_video_generation(user_id, user_text):
    if not rate_limiter.is_allowed(user_id, 'generation'):
        bot.send_message(user_id, "⚠️ Video generation limit cross ho gaya, thoda wait karo.")
        return
    
    conversation_memory.add_message(user_id, "user", f"Video: {user_text}")
    processing = bot.send_message(user_id, "🎥 Video ban rahi hai... 2-5 minute wait karo...")
    response = ai_client.generate_video(user_text, duration=10)
    
    if "error" not in response and "video_url" in response:
        try:
            bot.send_video(user_id, response["video_url"], caption=f"🎬 {user_text[:80]}...", parse_mode='Markdown')
            bot.delete_message(user_id, processing.message_id)
            conversation_memory.add_message(user_id, "bot", f"Video generated")
        except Exception as e:
            bot.edit_message_text(f"❌ Send error: {str(e)[:80]}", user_id, processing.message_id)
    else:
        bot.edit_message_text(f"❌ Video generation failed: {response.get('error', 'Unknown error')}", user_id, processing.message_id)


def run_code_generation(user_id, user_text):
    if not rate_limiter.is_allowed(user_id, 'standard'):
        bot.send_message(user_id, "⚠️ Code generation limit cross ho gaya.")
        return
    
    conversation_memory.add_message(user_id, "user", f"Code: {user_text}")
    bot.send_message(user_id, "💻 Code likh raha hoon...")
    response = ai_client.generate_code(user_text, language="python")
    
    if "error" not in response and "code" in response:
        code = response["code"]
        conversation_memory.add_message(user_id, "bot", "Code generated")
        if len(code) > 4096:
            for i in range(0, len(code), 4096):
                bot.send_message(user_id, f"```python\n{code[i:i+4096]}\n```", parse_mode='Markdown')
        else:
            bot.send_message(user_id, f"```python\n{code}\n```", parse_mode='Markdown')
    else:
        bot.send_message(user_id, f"❌ Code generation failed: {response.get('error', 'Unknown')}")


def run_translation(user_id, user_text):
    if not rate_limiter.is_allowed(user_id, 'standard'):
        bot.send_message(user_id, "⚠️ Translation limit cross ho gaya.")
        return
    
    conversation_memory.add_message(user_id, "user", f"Translate: {user_text}")
    bot.send_message(user_id, "🌐 Translate ho raha hai...")
    response = ai_client.translate(user_text, target_language="hindi")
    
    if "error" not in response and "translated_text" in response:
        translation = response["translated_text"]
        conversation_memory.add_message(user_id, "bot", translation)
        bot.send_message(user_id, f"✅ **Translated:**\n\n{translation}", parse_mode='Markdown')
    else:
        bot.send_message(user_id, f"❌ Translation failed: {response.get('error', 'Unknown')}")


def run_smart_chat(user_id, user_text):
    if not rate_limiter.is_allowed(user_id, 'standard'):
        bot.send_message(user_id, "⚠️ Rate limit cross ho gaya.")
        return
    
    conversation_memory.add_message(user_id, "user", user_text)
    thinking = bot.send_message(user_id, "💬 सोच रहा हूँ...")
    context = conversation_memory.get_context_string(user_id, last_n=3)
    response = ai_client.standard_chat(user_text, context)
    
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


# ============ DEFAULT HANDLER (PURE NLP + DETECTION) ============
@bot.message_handler(func=lambda m: True)
@error_handler
def handle_any_message(message):
    user_id = message.chat.id
    text = message.text or ""
    
    # Basic rate limit check
    if not rate_limiter.is_allowed(user_id, 'standard'):
        bot.send_message(user_id, "⚠️ Rate limit cross ho gaya, thoda wait karo.")
        return
    
    # Detect intent
    intent = intent_recognizer.recognize_intent(text)
    logger.info(f"User {user_id} intent: {intent}")
    
    if intent["type"] == "deep_thinking":
        run_deep_thinking(user_id, text)
    elif intent["type"] == "image":
        run_image_generation(user_id, text)
    elif intent["type"] == "video":
        run_video_generation(user_id, text)
    elif intent["type"] == "code":
        run_code_generation(user_id, text)
    elif intent["type"] == "translate":
        run_translation(user_id, text)
    else:
        run_smart_chat(user_id, text)


# ============ FLASK SERVER ============
def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ============ MAIN ============
if __name__ == "__main__":
    logger.info("""
╔═══════════════════════════════════════════════════╗
║  🚀 ULTIMATE ADVANCED TELEGRAM AI BOT v2.0 🚀    ║
║                                                   ║
║  Mode: PURE SMART (No Buttons, Full NLP Detect)   ║
╚═══════════════════════════════════════════════════╝
    """)
    logger.info(f"🔗 API URL: {AI_API_URL}")
    logger.info(f"🧠 Deep Thinking Model: {DEEP_THINKING_MODEL}")
    logger.info(f"💬 Standard Model: {STANDARD_MODEL}")
    logger.info(f"🌐 Flask Port: {PORT}")
    logger.info(f"📊 API Health: {'✅ HEALTHY' if ai_client.check_health() else '❌ OFFLINE'}")
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info(f"✅ Flask server started on port {PORT}")
    
    try:
        logger.info("🚀 Bot polling started...")
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        raise
