"""
Advanced Telegram Bot with AI Integration
- NLP Intent Recognition
- Interactive Buttons  
- Context Awareness
- Multi-language Support
- Conversation Memory (NEW!)

Author: AI Developer
Version: 1.1.0 - Added Conversation Memory
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

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '8401689004:AAEvNNZQJCoVh6UMwUGrKOUynDPd-1rsPAk')
AI_API_URL = os.getenv('AI_API_URL', 'https://ai-api-premium-server.onrender.com')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
PORT = int(os.getenv('PORT', 10000))
MAX_MEMORY_SIZE = 10  # Store last 10 messages per user

# Initialize bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Initialize Flask for health checks
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============ Flask Health Endpoint ============
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'running',
        'service': 'Telegram AI Bot with Memory',
        'version': '1.1.0',
        'features': ['conversation_memory', 'context_awareness'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health', methods=['GET'])
def health():
    api_health = ai_client.check_health() if 'ai_client' in globals() else False
    return jsonify({
        'bot': 'online',
        'api': 'healthy' if api_health else 'offline',
        'memory_users': len(conversation_memory.memory) if 'conversation_memory' in globals() else 0,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'bot_running': True,
        'telegram_api': 'connected',
        'ai_api_url': AI_API_URL,
        'features': ['memory', 'context'],
        'timestamp': datetime.now().isoformat()
    })

# ============ Conversation Memory System ============
class ConversationMemory:
    """Store and manage conversation history for each user"""
    
    def __init__(self, max_size=10):
        self.memory = {}  # {user_id: deque([{"role": "user/bot", "message": "...", "time": "..."}])}
        self.max_size = max_size
    
    def add_message(self, user_id, role, message):
        """Add a message to user's conversation history"""
        if user_id not in self.memory:
            self.memory[user_id] = deque(maxlen=self.max_size)
        
        self.memory[user_id].append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"Added to memory for user {user_id}: {role} - {message[:50]}...")
    
    def get_history(self, user_id, last_n=5):
        """Get last N messages from user's history"""
        if user_id not in self.memory:
            return []
        
        history = list(self.memory[user_id])
        return history[-last_n:] if len(history) > last_n else history
    
    def get_context_string(self, user_id, last_n=3):
        """Get conversation history as a formatted string for context"""
        history = self.get_history(user_id, last_n)
        if not history:
            return ""
        
        context = "\n\n--- Previous Conversation ---\n"
        for entry in history:
            role_label = "User" if entry["role"] == "user" else "Bot"
            context += f"{role_label}: {entry['message']}\n"
        context += "--- End Previous Conversation ---\n\n"
        
        return context
    
    def clear_history(self, user_id):
        """Clear conversation history for a user"""
        if user_id in self.memory:
            self.memory[user_id].clear()
            logger.info(f"Cleared memory for user {user_id}")
            return True
        return False
    
    def get_stats(self):
        """Get memory statistics"""
        total_users = len(self.memory)
        total_messages = sum(len(history) for history in self.memory.values())
        return {
            "total_users": total_users,
            "total_messages": total_messages,
            "max_size_per_user": self.max_size
        }

# Initialize conversation memory
conversation_memory = ConversationMemory(max_size=MAX_MEMORY_SIZE)

# ============ Rate Limiting ============
class RateLimiter:
    """Simple rate limiter for API requests"""
    
    def __init__(self, calls=10, period=60):
        self.calls = calls
        self.period = period
        self.user_calls = {}
    
    def is_allowed(self, user_id):
        """Check if user is within rate limit"""
        now = time()
        
        if user_id not in self.user_calls:
            self.user_calls[user_id] = []
        
        # Remove old calls outside period
        self.user_calls[user_id] = [
            call_time for call_time in self.user_calls[user_id]
            if now - call_time < self.period
        ]
        
        if len(self.user_calls[user_id]) < self.calls:
            self.user_calls[user_id].append(now)
            return True
        return False

rate_limiter = RateLimiter(calls=20, period=60)

# ============ NLP Intent Recognition System ============
class IntentRecognizer:
    """Advanced NLP for understanding user intent"""
    
    def __init__(self):
        self.intents = {
            "greeting": {
                "keywords": ["hello", "hi", "hey", "namaste", "salaam", "haan", "assalamu", 
                           "नमस्ते", "हाय", "हेलो"],
                "response_type": "greeting"
            },
            "help": {
                "keywords": ["help", "sahayata", "madad", "kya kar sakte ho", "features", 
                           "कैसे काम करता है", "मदद", "सहायता"],
                "response_type": "help"
            },
            "chat": {
                "keywords": ["baat karo", "chat", "conversation", "gup shup", "baatein",
                           "बातें", "गुप्शप", "बात"],
                "response_type": "chat"
            },
            "image": {
                "keywords": ["image", "photo", "picture", "tasveer", "draw", "banao", 
                           "generate", "तस्वीर", "फोटो"],
                "response_type": "image"
            },
            "code": {
                "keywords": ["code", "program", "python", "javascript", "likh do", "likho",
                           "कोड", "प्रोग्राम"],
                "response_type": "code"
            },
            "translate": {
                "keywords": ["translate", "hindi", "english", "spanish", "french", "anuvaad",
                           "अनुवाद", "अनुवाद करो"],
                "response_type": "translate"
            },
            "analyze": {
                "keywords": ["analyze", "analysis", "data", "samajh", "analyse karo",
                           "विश्लेषण", "डेटा"],
                "response_type": "analyze"
            }
        }
    
    def recognize_intent(self, text):
        """Identify user intent from text"""
        text_lower = text.lower()
        
        for intent, data in self.intents.items():
            for keyword in data["keywords"]:
                if keyword.lower() in text_lower:
                    return {
                        "intent": intent,
                        "type": data["response_type"],
                        "confidence": 0.85,
                        "original_text": text
                    }
        
        # Default to chat if no intent matched
        return {
            "intent": "general_query",
            "type": "chat",
            "confidence": 0.5,
            "original_text": text
        }

# ============ API Integration ============
class AIAPIClient:
    """Client for AI API interactions"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.timeout = 30
    
    def check_health(self):
        """Check API health"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def chat(self, message, model="claude-3", context=""):
        """AI Chat endpoint with context support"""
        try:
            # Add context to message if available
            full_message = context + message if context else message
            
            payload = {"message": full_message, "model": model, "max_tokens": 500}
            response = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            return {"error": f"API returned status {response.status_code}"}
        except Exception as e:
            logger.error(f"Chat API error: {e}")
            return {"error": str(e)}
    
    def generate_image(self, prompt, style="realistic"):
        """Image generation - simplified for demo"""
        logger.info(f"Image request: {prompt}")
        return {"error": "Image generation temporarily unavailable. Please use chat features."}
    
    def generate_code(self, description, language="python"):
        """Code generation endpoint"""
        try:
            payload = {"description": description, "language": language}
            response = requests.post(f"{self.base_url}/api/code", json=payload, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            return {"error": f"API returned status {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def translate(self, text, target_language="hindi"):
        """Translation endpoint"""
        try:
            payload = {"text": text, "target_language": target_language}
            response = requests.post(f"{self.base_url}/api/translate", json=payload, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            return {"error": f"API returned status {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

# Initialize components
intent_recognizer = IntentRecognizer()
ai_client = AIAPIClient(AI_API_URL)

# ============ Button Markup Builders ============
def get_main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        telebot.types.KeyboardButton("💬 Chat with AI"),
        telebot.types.KeyboardButton("💻 Generate Code"),
        telebot.types.KeyboardButton("🌐 Translate"),
        telebot.types.KeyboardButton("🧠 My Memory"),
        telebot.types.KeyboardButton("❓ Help")
    ]
    markup.add(*buttons)
    return markup

def get_chat_options():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        telebot.types.KeyboardButton("📝 Quick Chat"),
        telebot.types.KeyboardButton("🤔 Focused Question"),
        telebot.types.KeyboardButton("💡 Brainstorm"),
        telebot.types.KeyboardButton("⬅️ Back to Menu")
    ]
    markup.add(*buttons)
    return markup

def get_memory_options():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        telebot.types.KeyboardButton("📜 View History"),
        telebot.types.KeyboardButton("🗑️ Clear Memory"),
        telebot.types.KeyboardButton("⬅️ Back to Menu")
    ]
    markup.add(*buttons)
    return markup

# ============ Error Handler ============
def error_handler(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            bot.send_message(message.chat.id, f"❌ कुछ गलत हुआ। कृपया दोबारा कोशिश करें।", reply_markup=get_main_menu())
    return wrapper

# ============ Bot Commands ============
@bot.message_handler(commands=['start'])
@error_handler
def handle_start(message):
    user_name = message.from_user.first_name
    user_id = message.chat.id
    
    # Clear old memory on start
    conversation_memory.clear_history(user_id)
    
    welcome_text = f"""🤖 **Advanced AI Assistant Bot**

नमस्ते {user_name}! 👋

मैं एक Advanced AI Bot हूँ जो:
✅ आपके साथ Intelligent Chat कर सकता हूँ
✅ Code लिख सकता हूँ
✅ Language Translate कर सकता हूँ
✅ 🧠 **पिछली बातचीत याद रखता हूँ!**

**मुझे आप अपनी भाषा में कुछ भी बता सकते हो!**

क्या करना चाहते हो? नीचे दिए buttons से चुनो:"""
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode='Markdown')

@bot.message_handler(commands=['help'])
@error_handler
def handle_help(message):
    help_text = """📚 **उपलब्ध Features:**

1️⃣ **💬 Chat with AI** - किसी भी topic पर बातचीत करो
2️⃣ **💻 Generate Code** - किसी भी language में code लिखवाओ
3️⃣ **🌐 Translate** - 50+ languages में translation करो
4️⃣ **🧠 My Memory** - अपनी पिछली बातचीत देखो

**🧠 Memory Feature:**
- मैं आपकी last 10 बातों को याद रखता हूँ
- Context के साथ बेहतर जवाब देता हूँ
- आप अपनी history देख सकते हो
- Memory clear भी कर सकते हो

**कैसे use करें:**
- Main menu से कोई option चुनो
- अपनी request Hindi/English दोनों में दे सकते हो
- Bot automatically आपकी intent समझ लेगा

**उदाहरण:**
- "Python में factorial code लिख दो"
- "Hello को Hindi में translate करो"
- "पिछली बात याद है?"

🚀 मैं सब कुछ समझ जाऊंगा!"""
    
    bot.send_message(message.chat.id, help_text, reply_markup=get_main_menu(), parse_mode='Markdown')

@bot.message_handler(commands=['status'])
@error_handler
def handle_status(message):
    api_health = ai_client.check_health()
    memory_stats = conversation_memory.get_stats()
    
    status_text = f"""📊 **Bot Status:**

Bot: ✅ Online
API: {'✅ Healthy' if api_health else '❌ Offline'}
Memory: 🧠 Active

**Memory Stats:**
- Total Users: {memory_stats['total_users']}
- Total Messages: {memory_stats['total_messages']}
- Max Size/User: {memory_stats['max_size_per_user']}

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    
    bot.send_message(message.chat.id, status_text, parse_mode='Markdown')

@bot.message_handler(commands=['memory', 'history'])
@error_handler
def handle_memory_command(message):
    user_id = message.chat.id
    history = conversation_memory.get_history(user_id, last_n=10)
    
    if not history:
        bot.send_message(user_id, "🧠 अभी तक कोई conversation याद नहीं है।\n\nमेरे साथ बात करो, मैं याद रखूँगा!")
        return
    
    memory_text = "🧠 **Your Conversation History:**\n\n"
    for i, entry in enumerate(history, 1):
        role_emoji = "👤" if entry["role"] == "user" else "🤖"
        message_preview = entry["message"][:60] + "..." if len(entry["message"]) > 60 else entry["message"]
        memory_text += f"{i}. {role_emoji} {message_preview}\n"
    
    bot.send_message(user_id, memory_text, parse_mode='Markdown')

@bot.message_handler(commands=['clear'])
@error_handler
def handle_clear_command(message):
    user_id = message.chat.id
    conversation_memory.clear_history(user_id)
    bot.send_message(user_id, "🗑️ Memory cleared! \n\nअब मैं नई बातचीत शुरू करूँगा।")

# ============ Memory Menu Handler ============
@bot.message_handler(func=lambda m: "My Memory" in m.text)
@error_handler
def handle_memory_menu(message):
    user_id = message.chat.id
    memory_stats = conversation_memory.get_stats()
    user_history = conversation_memory.get_history(user_id)
    
    info_text = f"""🧠 **Memory Management**

आपकी memory में {len(user_history)} messages हैं।

**Options:**
- View History: अपनी पिछली बातें देखो
- Clear Memory: Memory को clear करो

क्या करना चाहते हो?"""
    
    bot.send_message(user_id, info_text, reply_markup=get_memory_options(), parse_mode='Markdown')

@bot.message_handler(func=lambda m: "View History" in m.text)
@error_handler
def handle_view_history(message):
    handle_memory_command(message)
    bot.send_message(message.chat.id, "\n और क्या?", reply_markup=get_memory_options())

@bot.message_handler(func=lambda m: "Clear Memory" in m.text)
@error_handler
def handle_clear_memory(message):
    handle_clear_command(message)
    bot.send_message(message.chat.id, "Main menu पर वापस जाएं:", reply_markup=get_main_menu())

# ============ Button Handlers ============
@bot.message_handler(func=lambda m: "Chat with AI" in m.text)
@error_handler
def handle_chat_mode(message):
    if not rate_limiter.is_allowed(message.chat.id):
        bot.send_message(message.chat.id, "⚠️ Rate limit exceeded. कृपया कुछ समय बाद कोशिश करें।")
        return
    
    msg = bot.send_message(message.chat.id, "💬 **Chat Mode शुरू हो गया!**\n\n🧠 मैं आपकी पिछली बातें याद रखूँगा।\n\nअब आप मुझसे कुछ भी पूछ सकते हो।\nएक सवाल लिखो:", 
                          reply_markup=get_chat_options(), parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_chat_message)

def process_chat_message(message):
    user_id = message.chat.id
    
    if "Back to Menu" in message.text:
        bot.send_message(user_id, "Main Menu पर वापस आ गए:", reply_markup=get_main_menu())
        return
    
    if not rate_limiter.is_allowed(user_id):
        bot.send_message(user_id, "⚠️ Rate limit exceeded.")
        return
    
    # Save user message to memory
    conversation_memory.add_message(user_id, "user", message.text)
    
    processing_msg = bot.send_message(user_id, "⏳ सोच रहा हूँ... (पिछली बातें याद रखते हुए)")
    
    # Get conversation context
    context = conversation_memory.get_context_string(user_id, last_n=3)
    
    # Get AI response with context
    response = ai_client.chat(message.text, context=context)
    
    if "error" not in response:
        ai_reply = response.get("response", "कोई reply नहीं मिला")
        
        # Save bot response to memory
        conversation_memory.add_message(user_id, "bot", ai_reply)
        
        bot.edit_message_text(ai_reply, user_id, processing_msg.message_id)
    else:
        bot.edit_message_text(f"❌ Error: {response['error']}", user_id, processing_msg.message_id)
    
    msg = bot.send_message(user_id, "\nकोई और सवाल? (मैं याद रखूँगा 🧠)", reply_markup=get_chat_options())
    bot.register_next_step_handler(msg, process_chat_message)

@bot.message_handler(func=lambda m: "Generate Code" in m.text)
@error_handler
def handle_code_mode(message):
    if not rate_limiter.is_allowed(message.chat.id):
        bot.send_message(message.chat.id, "⚠️ Rate limit exceeded.")
        return
    
    msg = bot.send_message(message.chat.id, "💻 **Code Generation Mode**\n\nक्या code चाहिए? Describe करो:\n(Example: 'Python में factorial function')", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_code_request)

def process_code_request(message):
    user_id = message.chat.id
    
    # Save to memory
    conversation_memory.add_message(user_id, "user", f"Code request: {message.text}")
    
    bot.send_message(user_id, "💻 Python में code लिखा जा रहा है...")
    response = ai_client.generate_code(message.text, "python")
    
    if "error" not in response and "code" in response:
        code = response["code"]
        
        # Save code to memory
        conversation_memory.add_message(user_id, "bot", f"Generated code: {code[:100]}...")
        
        if len(code) > 4096:
            for i in range(0, len(code), 4096):
                bot.send_message(user_id, f"```python\n{code[i:i+4096]}\n```", parse_mode='Markdown')
        else:
            bot.send_message(user_id, f"```python\n{code}\n```", parse_mode='Markdown')
    else:
        bot.send_message(user_id, f"❌ Code generation failed: {response.get('error', 'Unknown error')}")
    
    bot.send_message(user_id, "और कुछ?", reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: "Translate" in m.text)
@error_handler
def handle_translate_mode(message):
    if not rate_limiter.is_allowed(message.chat.id):
        bot.send_message(message.chat.id, "⚠️ Rate limit exceeded.")
        return
    
    msg = bot.send_message(message.chat.id, "🌐 **Translation Mode**\n\nक्या translate करना है? लिखो:\n(Example: 'Hello को Hindi में translate करो')")
    bot.register_next_step_handler(msg, process_translate_request)

def process_translate_request(message):
    user_id = message.chat.id
    
    # Save to memory
    conversation_memory.add_message(user_id, "user", f"Translate: {message.text}")
    
    bot.send_message(user_id, "🌐 Translate हो रहा है...")
    response = ai_client.translate(message.text, "hindi")
    
    if "error" not in response and "translated_text" in response:
        translation = response['translated_text']
        
        # Save to memory
        conversation_memory.add_message(user_id, "bot", f"Translation: {translation}")
        
        bot.send_message(user_id, f"✅ Translated:\n\n{translation}")
    else:
        bot.send_message(user_id, f"❌ Translation failed: {response.get('error', 'Unknown error')}")
    
    bot.send_message(user_id, "और translate करवाना है?", reply_markup=get_main_menu())

# ============ Default Handler with Memory ============
@bot.message_handler(func=lambda message: True)
@error_handler
def handle_any_message(message):
    user_id = message.chat.id
    
    if not rate_limiter.is_allowed(user_id):
        bot.send_message(user_id, "⚠️ Rate limit exceeded.")
        return
    
    intent_result = intent_recognizer.recognize_intent(message.text)
    logger.info(f"User {user_id}: Intent: {intent_result}")
    
    if intent_result["type"] == "greeting":
        # Check if user has history
        history = conversation_memory.get_history(user_id)
        greeting = "नमस्ते! 👋 कैसे हो?"
        if history:
            greeting += "\n\n🧠 मुझे आपकी पिछली बातें याद हैं!"
        greeting += "\n\nमैं कैसे मदद कर सकता हूँ?"
        bot.send_message(user_id, greeting, reply_markup=get_main_menu())
    elif intent_result["type"] == "help":
        handle_help(message)
    elif intent_result["type"] == "chat":
        handle_chat_mode(message)
    elif intent_result["type"] == "code":
        handle_code_mode(message)
    elif intent_result["type"] == "translate":
        handle_translate_mode(message)
    else:
        # Save user message
        conversation_memory.add_message(user_id, "user", message.text)
        
        processing_msg = bot.send_message(user_id, "⏳ सोच रहा हूँ... (context के साथ)")
        
        # Get context and response
        context = conversation_memory.get_context_string(user_id, last_n=3)
        response = ai_client.chat(message.text, context=context)
        
        if "error" not in response:
            ai_reply = response.get("response", "कोई reply नहीं मिला")
            
            # Save bot response
            conversation_memory.add_message(user_id, "bot", ai_reply)
            
            bot.edit_message_text(ai_reply, user_id, processing_msg.message_id)
        else:
            bot.edit_message_text(f"❌ Error: {response['error']}", user_id, processing_msg.message_id)

# ============ Start Flask Server in Thread ============
def run_flask():
    """Run Flask server in background thread"""
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ============ Main ============
if __name__ == "__main__":
    logger.info("🤖 Bot starting with Memory Feature...")
    logger.info(f"API URL: {AI_API_URL}")
    logger.info(f"Flask Port: {PORT}")
    logger.info(f"Memory Size: {MAX_MEMORY_SIZE} messages/user")
    logger.info(f"API Health: {ai_client.check_health()}")
    logger.info("✅ Bot started successfully with Memory!")
    
    # Start Flask in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info(f"✅ Flask server started on port {PORT}")
    
    # Start bot polling
    try:
        logger.info("🚀 Starting bot polling...")
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise
