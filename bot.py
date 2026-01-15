"""
Advanced Telegram Bot with AI Integration
- NLP Intent Recognition
- Interactive Buttons  
- Context Awareness
- Multi-language Support

Author: AI Developer
Version: 1.0.0
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

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '8401689004:AAEvNNZQJCoVh6UMwUGrKOUynDPd-1rsPAk')
AI_API_URL = os.getenv('AI_API_URL', 'https://ai-api-premium-server.onrender.com')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))  # Set this to your Telegram user ID
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Initialize bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
            response = requests.get(f"{self.base_url}/health", timeout=self.timeout)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Health check failed: {e}")
            return False
    
    def chat(self, message, model="claude-3"):
        """AI Chat endpoint"""
        try:
            payload = {
                "message": message,
                "model": model,
                "max_tokens": 500
            }
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout
            )
            return response.json()
        except Exception as e:
            logger.error(f"Chat API error: {e}")
            return {"error": str(e)}
    
    def generate_image(self, prompt, style="realistic"):
        """Image generation endpoint"""
        try:
            payload = {
                "prompt": prompt,
                "style": style,
                "size": "1024x1024"
            }
            response = requests.post(
                f"{self.base_url}/api/image",
                json=payload,
                timeout=self.timeout
            )
            return response.json()
        except Exception as e:
            logger.error(f"Image API error: {e}")
            return {"error": str(e)}
    
    def generate_code(self, description, language="python"):
        """Code generation endpoint"""
        try:
            payload = {
                "description": description,
                "language": language
            }
            response = requests.post(
                f"{self.base_url}/api/code",
                json=payload,
                timeout=self.timeout
            )
            return response.json()
        except Exception as e:
            logger.error(f"Code API error: {e}")
            return {"error": str(e)}
    
    def translate(self, text, target_language="hindi"):
        """Translation endpoint"""
        try:
            payload = {
                "text": text,
                "target_language": target_language
            }
            response = requests.post(
                f"{self.base_url}/api/translate",
                json=payload,
                timeout=self.timeout
            )
            return response.json()
        except Exception as e:
            logger.error(f"Translate API error: {e}")
            return {"error": str(e)}

# Initialize components
intent_recognizer = IntentRecognizer()
ai_client = AIAPIClient(AI_API_URL)

# ============ Button Markup Builders ============
def get_main_menu():
    """Main menu with interactive buttons"""
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        telebot.types.KeyboardButton("💬 Chat with AI"),
        telebot.types.KeyboardButton("🎨 Generate Image"),
        telebot.types.KeyboardButton("💻 Generate Code"),
        telebot.types.KeyboardButton("🌐 Translate"),
        telebot.types.KeyboardButton("📊 Analyze Data"),
        telebot.types.KeyboardButton("❓ Help")
    ]
    markup.add(*buttons)
    return markup

def get_chat_options():
    """Chat mode options"""
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        telebot.types.KeyboardButton("📝 Quick Chat"),
        telebot.types.KeyboardButton("🤔 Focused Question"),
        telebot.types.KeyboardButton("💡 Brainstorm"),
        telebot.types.KeyboardButton("⬅️ Back to Menu")
    ]
    markup.add(*buttons)
    return markup

def get_image_styles():
    """Image generation styles"""
    markup = telebot.types.InlineKeyboardMarkup()
    buttons = [
        telebot.types.InlineKeyboardButton("🎨 Realistic", callback_data="img_realistic"),
        telebot.types.InlineKeyboardButton("🌈 Artistic", callback_data="img_artistic"),
        telebot.types.InlineKeyboardButton("🎮 3D Render", callback_data="img_3d"),
        telebot.types.InlineKeyboardButton("✨ Fantasy", callback_data="img_fantasy"),
    ]
    markup.add(*buttons)
    return markup

def get_code_languages():
    """Programming languages for code generation"""
    markup = telebot.types.InlineKeyboardMarkup()
    buttons = [
        telebot.types.InlineKeyboardButton("🐍 Python", callback_data="code_python"),
        telebot.types.InlineKeyboardButton("📚 JavaScript", callback_data="code_javascript"),
        telebot.types.InlineKeyboardButton("☕ Java", callback_data="code_java"),
        telebot.types.InlineKeyboardButton("🦀 Rust", callback_data="code_rust"),
    ]
    markup.add(*buttons)
    return markup

# ============ Error Handler Decorator ============
def error_handler(func):
    """Decorator for handling errors gracefully"""
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            bot.send_message(
                message.chat.id,
                f"❌ कुछ गलत हुआ। कृपया दोबारा कोशिश करें।\n\nError: {type(e).__name__}",
                reply_markup=get_main_menu()
            )
    return wrapper

# ============ Bot Commands ============
@bot.message_handler(commands=['start'])
@error_handler
def handle_start(message):
    """Start command - Welcome message"""
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    
    welcome_text = f"""🤖 **Advanced AI Assistant Bot**

नमस्ते {user_name}! 👋

मैं एक Advanced AI Bot हूँ जो:
✅ आपके साथ Intelligent Chat कर सकता हूँ
✅ Images Generate कर सकता हूँ
✅ Code लिख सकता हूँ
✅ Language Translate कर सकता हूँ
✅ Data को Analyze कर सकता हूँ

**मुझे आप अपनी भाषा में कुछ भी बता सकते हो!**

क्या करना चाहते हो? नीचे दिए buttons से चुनो:"""
    
    bot.send_message(chat_id, welcome_text, reply_markup=get_main_menu(), parse_mode='Markdown')

@bot.message_handler(commands=['help'])
@error_handler
def handle_help(message):
    """Help command"""
    chat_id = message.chat.id
    help_text = """📚 **उपलब्ध Features:**

1️⃣ **💬 Chat with AI** - किसी भी topic पर बातचीत करो
2️⃣ **🎨 Generate Image** - अपनी सोच के according image बनवाओ
3️⃣ **💻 Generate Code** - किसी भी language में code लिखवाओ
4️⃣ **🌐 Translate** - 50+ languages में translation करो
5️⃣ **📊 Analyze Data** - Data analysis और insights लो

**कैसे use करें:**
- Main menu से कोई option चुनो
- अपनी request Hindi/English दोनों में दे सकते हो
- Bot automatically आपकी intent समझ लेगा

**उदाहरण:**
- "मुझे एक mountain की image चाहिए"
- "Python में factorial code लिख दो"
- "Hello को Hindi में translate करो"

🚀 मैं सब कुछ समझ जाऊंगा!"""
    
    bot.send_message(chat_id, help_text, reply_markup=get_main_menu(), parse_mode='Markdown')

@bot.message_handler(commands=['status'])
@error_handler
def handle_status(message):
    """Check bot and API status"""
    chat_id = message.chat.id
    
    api_health = ai_client.check_health()
    status_text = f"""📊 **Bot Status:**

Bot: ✅ Online
API: {'✅ Healthy' if api_health else '❌ Offline'}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    bot.send_message(chat_id, status_text, parse_mode='Markdown')

# ============ Main Button Handlers ============
@bot.message_handler(func=lambda message: "Chat with AI" in message.text)
@error_handler
def handle_chat_mode(message):
    """Enter chat mode"""
    chat_id = message.chat.id
    
    if not rate_limiter.is_allowed(chat_id):
        bot.send_message(chat_id, "⚠️ Rate limit exceeded. कृपया कुछ समय बाद कोशिश करें।")
        return
    
    msg = bot.send_message(
        chat_id, 
        "💬 **Chat Mode शुरू हो गया!**\n\nअब आप मुझसे कुछ भी पूछ सकते हो।\nएक सवाल लिखो:",
        reply_markup=get_chat_options(), 
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_chat_message)

def process_chat_message(message):
    """Process chat messages"""
    chat_id = message.chat.id
    user_text = message.text
    
    if "Back to Menu" in user_text:
        bot.send_message(chat_id, "Main Menu पर वापस आ गए:", reply_markup=get_main_menu())
        return
    
    if not rate_limiter.is_allowed(chat_id):
        bot.send_message(chat_id, "⚠️ Rate limit exceeded. कृपया कुछ समय बाद कोशिश करें।")
        return
    
    # Show processing indicator
    processing_msg = bot.send_message(chat_id, "⏳ सोच रहा हूँ... एक सेकंड रुको...")
    
    # Get AI response
    response = ai_client.chat(user_text)
    
    if "error" not in response:
        ai_reply = response.get("response", "कोई reply नहीं मिला")
        bot.edit_message_text(ai_reply, chat_id, processing_msg.message_id)
    else:
        bot.edit_message_text(
            f"❌ Error: {response['error']}",
            chat_id, 
            processing_msg.message_id
        )
    
    # Ask for next message
    msg = bot.send_message(chat_id, "\nकोई और सवाल?", reply_markup=get_chat_options())
    bot.register_next_step_handler(msg, process_chat_message)

@bot.message_handler(func=lambda message: "Generate Image" in message.text)
@error_handler
def handle_image_mode(message):
    """Image generation mode"""
    chat_id = message.chat.id
    
    if not rate_limiter.is_allowed(chat_id):
        bot.send_message(chat_id, "⚠️ Rate limit exceeded.")
        return
    
    msg = bot.send_message(
        chat_id, 
        "🎨 **Image Generation Mode**\n\nअपना image description लिखो:\n(Example: 'एक सुंदर mountain sunset')",
        reply_markup=get_image_styles()
    )
    bot.register_next_step_handler(msg, process_image_request)

def process_image_request(message):
    """Process image generation request"""
    chat_id = message.chat.id
    prompt = message.text
    
    bot.send_message(chat_id, "🎨 Image बनाई जा रही है... कुछ सेकंड का इंतजार करो...")
    
    response = ai_client.generate_image(prompt, "realistic")
    
    if "error" not in response and "image_url" in response:
        bot.send_photo(chat_id, response["image_url"], caption=f"✨ {prompt}")
    else:
        bot.send_message(chat_id, f"❌ Image generation failed: {response.get('error', 'Unknown error')}")
    
    bot.send_message(chat_id, "अगर कुछ और चाहिए?", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: "Generate Code" in message.text)
@error_handler
def handle_code_mode(message):
    """Code generation mode"""
    chat_id = message.chat.id
    
    if not rate_limiter.is_allowed(chat_id):
        bot.send_message(chat_id, "⚠️ Rate limit exceeded.")
        return
    
    msg = bot.send_message(
        chat_id, 
        "💻 **Code Generation Mode**\n\nक्या code चाहिए? Describe करो:\n(Example: 'Python में factorial function')",
        reply_markup=get_code_languages()
    )
    bot.register_next_step_handler(msg, process_code_request)

def process_code_request(message):
    """Process code generation request"""
    chat_id = message.chat.id
    description = message.text
    
    bot.send_message(chat_id, f"💻 Python में code लिखा जा रहा है...")
    
    response = ai_client.generate_code(description, "python")
    
    if "error" not in response and "code" in response:
        code = response["code"]
        # Split into chunks if too long
        if len(code) > 4096:
            for i in range(0, len(code), 4096):
                bot.send_message(chat_id, f"```python\n{code[i:i+4096]}\n```", parse_mode='Markdown')
        else:
            bot.send_message(chat_id, f"```python\n{code}\n```", parse_mode='Markdown')
    else:
        bot.send_message(chat_id, f"❌ Code generation failed: {response.get('error', 'Unknown error')}")
    
    bot.send_message(chat_id, "और कुछ?", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: "Translate" in message.text)
@error_handler
def handle_translate_mode(message):
    """Translation mode"""
    chat_id = message.chat.id
    
    if not rate_limiter.is_allowed(chat_id):
        bot.send_message(chat_id, "⚠️ Rate limit exceeded.")
        return
    
    msg = bot.send_message(
        chat_id, 
        "🌐 **Translation Mode**\n\nक्या translate करना है? लिखो:\n(Example: 'Hello को Hindi में translate करो')"
    )
    bot.register_next_step_handler(msg, process_translate_request)

def process_translate_request(message):
    """Process translation request"""
    chat_id = message.chat.id
    text = message.text
    
    bot.send_message(chat_id, "🌐 Translate हो रहा है...")
    
    response = ai_client.translate(text, "hindi")
    
    if "error" not in response and "translated_text" in response:
        bot.send_message(chat_id, f"✅ Translated:\n\n{response['translated_text']}")
    else:
        bot.send_message(chat_id, f"❌ Translation failed: {response.get('error', 'Unknown error')}")
    
    bot.send_message(chat_id, "और translate करवाना है?", reply_markup=get_main_menu())

# ============ Default Handler for any text ============
@bot.message_handler(func=lambda message: True)
@error_handler
def handle_any_message(message):
    """Handle any message with NLP intent recognition"""
    chat_id = message.chat.id
    user_text = message.text
    
    if not rate_limiter.is_allowed(chat_id):
        bot.send_message(chat_id, "⚠️ Rate limit exceeded. कृपया कुछ समय बाद कोशिश करें।")
        return
    
    # Recognize intent
    intent_result = intent_recognizer.recognize_intent(user_text)
    logger.info(f"User {chat_id}: Intent detected: {intent_result}")
    
    if intent_result["type"] == "greeting":
        response = "नमस्ते! 👋 कैसे हो? मैं कैसे मदद कर सकता हूँ?"
        bot.send_message(chat_id, response, reply_markup=get_main_menu())
    
    elif intent_result["type"] == "help":
        handle_help(message)
    
    elif intent_result["type"] == "chat":
        bot.send_message(chat_id, "💬 Chat mode में जा रहे हैं...", reply_markup=get_main_menu())
        handle_chat_mode(message)
    
    elif intent_result["type"] == "image":
        handle_image_mode(message)
    
    elif intent_result["type"] == "code":
        handle_code_mode(message)
    
    elif intent_result["type"] == "translate":
        handle_translate_mode(message)
    
    else:
        # Default: treat as chat
        processing_msg = bot.send_message(chat_id, "⏳ सोच रहा हूँ...")
        
        response = ai_client.chat(user_text)
        
        if "error" not in response:
            ai_reply = response.get("response", "कोई reply नहीं मिला")
            bot.edit_message_text(ai_reply, chat_id, processing_msg.message_id)
        else:
            bot.edit_message_text(
                f"❌ Error: {response['error']}",
                chat_id,
                processing_msg.message_id
            )

# ============ Start Bot ============
if __name__ == "__main__":
    logger.info("🤖 Bot starting...")
    logger.info(f"API Health: {ai_client.check_health()}")
    logger.info("✅ Bot started successfully!")
    logger.info(f"Bot running with token: {TELEGRAM_TOKEN[:20]}...")
    
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise
