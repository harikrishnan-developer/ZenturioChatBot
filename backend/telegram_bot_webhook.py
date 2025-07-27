import os
import asyncio
import time
import re
import httpx
from fastapi import FastAPI, Request, HTTPException
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import RetryAfter
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your Render app URL + /webhook
BACKEND_URL = os.getenv("BACKEND_URL", "https://your-backend-url.onrender.com/ask")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is required")
if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL environment variable is required")

# FastAPI app for webhook
app = FastAPI()

# Telegram application
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

# Track running tasks per user
user_tasks = {}
user_last_message = {}
RATE_LIMIT_SECONDS = 2

async def safe_send_message(bot: Bot, chat_id: int, text: str, max_retries=3):
    """Safely send a message with retry logic and rate limiting"""
    text = text.replace('###', '')
    current_time = time.time()
    
    # Check rate limiting
    if chat_id in user_last_message:
        time_since_last = current_time - user_last_message[chat_id]
        if time_since_last < RATE_LIMIT_SECONDS:
            await asyncio.sleep(RATE_LIMIT_SECONDS - time_since_last)
    
    # Try to send message with exponential backoff
    for attempt in range(max_retries):
        try:
            message = await bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
            user_last_message[chat_id] = time.time()
            return message
        except RetryAfter as e:
            if attempt < max_retries - 1:
                wait_time = min(e.retry_after + (attempt * 5), 120)
                print(f"Rate limited, waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print(f"Failed to send message after {max_retries} attempts")
                return None
        except Exception as e:
            print(f"Error sending message: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
            else:
                return None

async def safe_edit_message(bot: Bot, chat_id: int, message_id: int, text: str, max_retries=3, parse_mode=None):
    """Safely edit a message with retry logic"""
    text = text.replace('###', '')
    
    for attempt in range(max_retries):
        try:
            if parse_mode:
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode=parse_mode)
            else:
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
            return True
        except RetryAfter as e:
            if attempt < max_retries - 1:
                wait_time = min(e.retry_after + (attempt * 5), 120)
                print(f"Rate limited during edit, waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print(f"Failed to edit message after {max_retries} attempts")
                return False
        except Exception as e:
            if "Message is not modified" not in str(e):
                print(f"Error editing message: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
            else:
                return False

def sanitize_markdown(text):
    text = re.sub(r'(?<!\*)\*(?!\*)', '', text)
    text = re.sub(r'(?<!_)_(?!_)', '', text)
    text = re.sub(r'\[([^\]]*)\]\(([^\)]*)$', r'\1 (\2)', text)
    text = re.sub(r'`+', '', text)
    return text

def format_for_telegram(text):
    text = re.sub(r'^#+\s*(.+)$', r'*\1*', text, flags=re.MULTILINE)
    text = re.sub(r'^[\-*]\s+', '\u2022 ', text, flags=re.MULTILINE)
    text = re.sub(r'^(\d+)\.\s*', r'\1. ', text, flags=re.MULTILINE)
    text = re.sub(r'(\n\*.+\*)', r'\n\1', text)
    text = re.sub(r'#+', '', text)
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_send_message(context.bot, update.effective_chat.id, "Hello! I am your LLM-powered assistant. Ask me about government services.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task = user_tasks.get(user_id)
    if task and not task.done():     
        task.cancel()
        await safe_send_message(context.bot, update.effective_chat.id, "Generation stopped.")
    else:
        await safe_send_message(context.bot, update.effective_chat.id, "No active generation to stop.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    async def stream_and_edit():
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                async with client.stream("POST", BACKEND_URL, json={"message": user_message}) as response:
                    partial_reply = ""
                    sent_message = await safe_send_message(context.bot, chat_id, "...")
                    if not sent_message:
                        print("Failed to send initial message")
                        return
                    
                    last_edit_time = time.time()
                    edit_interval = 0.2
                    
                    async for chunk in response.aiter_text():
                        if chunk:
                            tokens = re.findall(r'\n|\S+', chunk)
                            for token in tokens:
                                if token == '\n':
                                    partial_reply += '\n'
                                else:
                                    if partial_reply and not partial_reply.endswith((' ', '\n')):
                                        partial_reply += ' '
                                    partial_reply += token
                                
                                if time.time() - last_edit_time > edit_interval:
                                    await safe_edit_message(context.bot, chat_id, sent_message.message_id, partial_reply)
                                    last_edit_time = time.time()
                    
                    # Final edit with complete response
                    if partial_reply:
                        clean_reply = sanitize_markdown(partial_reply)
                        formatted_reply = format_for_telegram(clean_reply)
                        await safe_edit_message(context.bot, chat_id, sent_message.message_id, formatted_reply, parse_mode='Markdown')
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Error in stream_and_edit: {e}")
    
    # Cancel any previous task for this user
    prev_task = user_tasks.get(user_id)
    if prev_task and not prev_task.done():
        prev_task.cancel()
    
    # Start new task
    task = asyncio.create_task(stream_and_edit())
    user_tasks[user_id] = task

# Add handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("stop", stop))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming webhook updates from Telegram"""
    try:
        # Get the raw body
        body = await request.body()
        
        # Parse the update
        update = Update.de_json(data=await request.json(), bot=telegram_app.bot)
        
        # Process the update
        await telegram_app.process_update(update)
        
        return {"status": "ok"}
    except Exception as e:
        print(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Telegram Bot Webhook Server is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

async def set_webhook():
    """Set the webhook URL for the bot"""
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        webhook_info = await bot.get_webhook_info()
        
        if webhook_info.url != WEBHOOK_URL:
            print(f"Setting webhook to: {WEBHOOK_URL}")
            await bot.set_webhook(url=WEBHOOK_URL)
            print("Webhook set successfully!")
        else:
            print("Webhook already set correctly")
            
    except Exception as e:
        print(f"Error setting webhook: {e}")

@app.on_event("startup")
async def startup_event():
    """Initialize the bot and set webhook on startup"""
    await telegram_app.initialize()
    await set_webhook()
    print("Telegram bot webhook server started!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await telegram_app.shutdown()
    print("Telegram bot webhook server stopped!")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)