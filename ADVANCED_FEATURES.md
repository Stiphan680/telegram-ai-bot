# 🔧 Advanced Features & Customization Guide

## 🤬 Table of Contents

1. [NLP Intent Recognition](#nlp-intent-recognition)
2. [Custom Intent Adding](#custom-intent-adding)
3. [Database Integration](#database-integration)
4. [User Analytics](#user-analytics)
5. [Rate Limiting & Quotas](#rate-limiting--quotas)
6. [Webhook Setup](#webhook-setup)
7. [Admin Commands](#admin-commands)
8. [Error Handling](#error-handling)
9. [Performance Optimization](#performance-optimization)

---

## 🤬 NLP Intent Recognition

### Current Intent System

```python
intents = {
    "greeting": {"keywords": ["hello", "hi", "namaste"], "response_type": "greeting"},
    "help": {"keywords": ["help", "sahayata"], "response_type": "help"},
    "chat": {"keywords": ["baat karo"], "response_type": "chat"},
    "image": {"keywords": ["image", "picture"], "response_type": "image"},
    "code": {"keywords": ["code", "program"], "response_type": "code"},
    "translate": {"keywords": ["translate"], "response_type": "translate"},
    "analyze": {"keywords": ["analyze"], "response_type": "analyze"}
}
```

### How It Works

```
User Message
    │
    ▼
Keyword Matching (Case-insensitive)
    │
    ▼
Confidence Scoring
    │
    ▼
Intent Assignment
    │
    ▼
Appropriate Handler Execution
```

### Confidence Levels

```python
Confidence >= 0.85  → High confidence (exact match)
0.50 <= Confidence < 0.85  → Medium confidence (partial match)
Confidence < 0.50  → Fallback to general chat
```

---

## 🔧 Custom Intent Adding

### Add New Intent

```python
# bot.py में IntentRecognizer class में add karo

self.intents["music"] = {
    "keywords": ["song", "music", "gaana", "geet", "music player"],
    "response_type": "music"
}

self.intents["weather"] = {
    "keywords": ["weather", "mausam", "temperature", "barish"],
    "response_type": "weather"
}

self.intents["news"] = {
    "keywords": ["news", "khabar", "latest", "breaking"],
    "response_type": "news"
}
```

### Add Handler for New Intent

```python
@bot.message_handler(func=lambda message: handle_music_intent(message))
def handle_music_mode(message):
    """Music request handler"""
    chat_id = message.chat.id
    query = message.text
    
    bot.send_message(chat_id, "🎵 Music search ho raha hai...")
    
    # Aapka music API call
    music_results = search_music(query)
    
    # Display results with buttons
    markup = telebot.types.InlineKeyboardMarkup()
    for track in music_results[:5]:
        btn = telebot.types.InlineKeyboardButton(
            text=track['title'],
            callback_data=f"play_{track['id']}"
        )
        markup.add(btn)
    
    bot.send_message(chat_id, "🎶 Ye tracks mile:", reply_markup=markup)
```

---

## 📊 Database Integration

### SQLite (Simple)

```python
import sqlite3

class UserDatabase:
    def __init__(self, db_path='users.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create database schema"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT,
                response TEXT,
                intent TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        self.conn.commit()
    
    def add_user(self, user_id, first_name, last_name, username):
        """Add new user"""
        try:
            self.cursor.execute('''
                INSERT INTO users (user_id, first_name, last_name, username)
                VALUES (?, ?, ?, ?)
            ''', (user_id, first_name, last_name, username))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # User already exists
    
    def save_conversation(self, user_id, message, response, intent):
        """Save user conversation"""
        self.cursor.execute('''
            INSERT INTO conversations (user_id, message, response, intent)
            VALUES (?, ?, ?, ?)
        ''', (user_id, message, response, intent))
        self.conn.commit()
    
    def get_user_history(self, user_id, limit=10):
        """Get user conversation history"""
        self.cursor.execute('''
            SELECT message, response, intent, timestamp
            FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        return self.cursor.fetchall()

# Usage
db = UserDatabase()

@bot.message_handler(commands=['start'])
def handle_start(message):
    user = message.from_user
    db.add_user(user.id, user.first_name, user.last_name, user.username)
    # ... rest of code
```

### PostgreSQL (Production)

```python
import psycopg2
from psycopg2.extras import RealDictCursor

class ProductionDatabase:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)
    
    def add_user(self, user_id, first_name, last_name, username):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
                INSERT INTO users (user_id, first_name, last_name, username)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) DO NOTHING
            ''', (user_id, first_name, last_name, username))
            self.conn.commit()
```

---

## 📊 User Analytics

```python
from collections import defaultdict
from datetime import datetime, timedelta

class Analytics:
    def __init__(self):
        self.user_commands = defaultdict(list)
        self.intent_usage = defaultdict(int)
        self.daily_active_users = set()
    
    def track_command(self, user_id, command, timestamp=None):
        """Track user command usage"""
        if timestamp is None:
            timestamp = datetime.now()
        
        self.user_commands[user_id].append({
            'command': command,
            'timestamp': timestamp
        })
        self.daily_active_users.add(user_id)
    
    def track_intent(self, intent):
        """Track intent usage"""
        self.intent_usage[intent] += 1
    
    def get_stats(self):
        """Get analytics summary"""
        total_users = len(self.user_commands)
        daily_active = len(self.daily_active_users)
        total_commands = sum(len(cmds) for cmds in self.user_commands.values())
        
        most_used_intent = max(self.intent_usage.items(), key=lambda x: x[1])[0]
        
        return {
            'total_users': total_users,
            'daily_active_users': daily_active,
            'total_commands': total_commands,
            'most_used_intent': most_used_intent
        }
    
    def get_user_stats(self, user_id):
        """Get individual user stats"""
        user_cmds = self.user_commands.get(user_id, [])
        return {
            'total_commands': len(user_cmds),
            'commands': [cmd['command'] for cmd in user_cmds[-10:]]  # Last 10
        }

# Usage
analytics = Analytics()

@bot.message_handler(func=lambda message: True)
def handle_any_message(message):
    analytics.track_command(message.from_user.id, message.text)
    intent_result = intent_recognizer.recognize_intent(message.text)
    analytics.track_intent(intent_result['intent'])
    # ... rest of code

# Stats dekhne ke liye
@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id == ADMIN_ID:
        stats = analytics.get_stats()
        stats_text = f"""📊 **Bot Statistics**
        
Total Users: {stats['total_users']}
Daily Active: {stats['daily_active_users']}
Total Commands: {stats['total_commands']}
Most Used Intent: {stats['most_used_intent']}
        """
        bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')
```

---

## 💨 Rate Limiting & Quotas

```python
from functools import wraps
from time import time

class RateLimiter:
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
    
    def get_remaining(self, user_id):
        """Get remaining calls for user"""
        now = time()
        self.user_calls[user_id] = [
            call_time for call_time in self.user_calls.get(user_id, [])
            if now - call_time < self.period
        ]
        return max(0, self.calls - len(self.user_calls[user_id]))

# Usage
rate_limiter = RateLimiter(calls=20, period=60)  # 20 calls per minute

def rate_limit_handler(func):
    @wraps(func)
    def wrapper(message):
        if not rate_limiter.is_allowed(message.from_user.id):
            remaining = rate_limiter.get_remaining(message.from_user.id)
            bot.send_message(
                message.chat.id,
                f"⚠️ Rate limit exceeded.\nTry again in {60} seconds."
            )
            return
        return func(message)
    return wrapper

@bot.message_handler(func=lambda m: "image" in m.text.lower())
@rate_limit_handler
def handle_image_mode(message):
    # Image generation code
    pass
```

---

## 🏃‍♂️ Webhook Setup (Fast)

Polling ke bajay webhooks use karo (faster responses):

```python
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook from Telegram"""
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# Setup webhook
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://your-domain.com/webhook')
    app.run(host='0.0.0.0', port=443)
```

---

## 🔐 Admin Commands

```python
ADMIN_ID = 123456789  # Your user ID

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Unauthorized")
        return
    
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(
        telebot.types.KeyboardButton("📊 Stats"),
        telebot.types.KeyboardButton("📄 Logs"),
        telebot.types.KeyboardButton(🗣️ Broadcast")
    )
    bot.send_message(message.chat.id, "Admin Panel", reply_markup=markup)

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and "Stats" in m.text)
def admin_stats(message):
    stats = analytics.get_stats()
    bot.send_message(
        message.chat.id,
        f"Users: {stats['total_users']}\nDaily Active: {stats['daily_active_users']}"
    )

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and "Broadcast" in m.text)
def admin_broadcast(message):
    msg = bot.send_message(message.chat.id, "Enter broadcast message:")
    bot.register_next_step_handler(msg, do_broadcast)

def do_broadcast(message):
    # Broadcast to all users
    for user_id in db.get_all_users():
        try:
            bot.send_message(user_id, message.text)
        except:
            pass  # User blocked bot
```

---

## 🛡️ Error Handling

```python
import traceback
from logging import getLogger

logger = getLogger(__name__)

def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Notify user
            if args and hasattr(args[0], 'chat'):
                message = args[0]
                bot.send_message(
                    message.chat.id,
                    f"❌ Something went wrong. Please try again.\n
Error: {type(e).__name__}"
                )
    return wrapper

# Usage
@bot.message_handler(func=lambda m: True)
@error_handler
def handle_any_message(message):
    # Your code here
    pass
```

---

## 🚀 Performance Optimization

### 1. Response Caching

```python
from functools import lru_cache
import hashlib

class ResponseCache:
    def __init__(self, ttl=3600):
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key):
        if key in self.cache:
            return self.cache[key]['data']
        return None
    
    def set(self, key, value):
        self.cache[key] = {
            'data': value,
            'timestamp': time()
        }
    
    def cleanup(self):
        """Remove expired entries"""
        now = time()
        self.cache = {
            k: v for k, v in self.cache.items()
            if now - v['timestamp'] < self.ttl
        }

cache = ResponseCache(ttl=300)  # 5 minute TTL

def cached_response(func):
    @wraps(func)
    def wrapper(query):
        cache_key = hashlib.md5(query.encode()).hexdigest()
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        result = func(query)
        cache.set(cache_key, result)
        return result
    
    return wrapper

@cached_response
def get_ai_response(query):
    return ai_client.chat(query)
```

### 2. Async Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)

def run_async(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))
    return wrapper

async def process_image_async(prompt):
    return await ai_client.generate_image_async(prompt)
```

### 3. Lazy Loading

```python
class LazyLoader:
    def __init__(self, obj):
        self._obj = obj
        self._loaded = False
    
    def __getattr__(self, name):
        if not self._loaded:
            # Initialize expensive resources
            self._obj.initialize()
            self._loaded = True
        return getattr(self._obj, name)
```

---

**Happy Advanced Coding! 🙋**
