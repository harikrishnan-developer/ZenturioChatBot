import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
import httpx
import time
from telegram.error import RetryAfter, NetworkError
import re
import os
from dotenv import load_dotenv

load_dotenv()

# Track running tasks per user
user_tasks = {}
# Track last message time per user to implement rate limiting
user_last_message = {}

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7323234298:AAEEyIjq0TK92C6oOaPCOukIdqQKCkmqimM")
BACKEND_URL = "http://127.0.0.1:8000/ask"

# Rate limiting: minimum seconds between messages per user
RATE_LIMIT_SECONDS = 2

async def safe_send_message(update: Update, text: str, max_retries=3):
    """Safely send a message with retry logic and rate limiting"""
    text = text.replace('###', '')
    user_id = update.effective_user.id
    current_time = time.time()
    
    # Check rate limiting
    if user_id in user_last_message:
        time_since_last = current_time - user_last_message[user_id]
        if time_since_last < RATE_LIMIT_SECONDS:
            await asyncio.sleep(RATE_LIMIT_SECONDS - time_since_last)
    
    # Try to send message with exponential backoff
    for attempt in range(max_retries):
        try:
            message = await update.message.reply_text(text, parse_mode='Markdown')
            user_last_message[user_id] = time.time()
            return message
        except RetryAfter as e:
            if attempt < max_retries - 1:
                # Use Telegram's suggested retry time, but cap it at a reasonable maximum
                wait_time = min(e.retry_after + (attempt * 5), 120)  # Max 2 minutes
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

# Update safe_edit_message to accept parse_mode argument
default_parse_mode = None
async def safe_edit_message(message, text: str, max_retries=3, parse_mode=default_parse_mode):
    """Safely edit a message with retry logic"""
    text = text.replace('###', '')
    # Check if content is actually different to avoid "Message is not modified" error
    try:
        if message.text == text:
            return True  # No need to edit if content is the same
    except:
        pass  # If we can't check current text, proceed with edit
    
    for attempt in range(max_retries):
        try:
            if parse_mode:
                await message.edit_text(text, parse_mode=parse_mode)
            else:
                await message.edit_text(text)
            return True
        except RetryAfter as e:
            if attempt < max_retries - 1:
                # Use Telegram's suggested retry time, but cap it at a reasonable maximum
                wait_time = min(e.retry_after + (attempt * 5), 120)  # Max 2 minutes
                print(f"Rate limited during edit, waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print(f"Failed to edit message after {max_retries} attempts")
                return False
        except Exception as e:
            # Don't log "Message is not modified" errors as they're harmless
            if "Message is not modified" not in str(e):
                print(f"Error editing message: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
            else:
                return False

def sanitize_markdown(text):
    # Remove unmatched single asterisks and underscores
    text = re.sub(r'(?<!\*)\*(?!\*)', '', text)  # Remove single *
    text = re.sub(r'(?<!_)_(?!_)', '', text)        # Remove single _
    # Remove incomplete links (unclosed [ or () )
    text = re.sub(r'\[([^\]]*)\]\(([^\)]*)$', r'\1 (\2)', text)
    # Optionally, remove stray backticks
    text = re.sub(r'`+', '', text)
    return text

def format_for_telegram(text):
    # Headings: convert lines starting with # or ## to bold
    text = re.sub(r'^#+\s*(.+)$', r'*\1*', text, flags=re.MULTILINE)
    # Bullet points: convert lines starting with - or * to •
    text = re.sub(r'^[\-*]\s+', '\u2022 ', text, flags=re.MULTILINE)
    # Numbered lists: ensure numbers are followed by a period and space
    text = re.sub(r'^(\d+)\.\s*', r'\1. ', text, flags=re.MULTILINE)
    # Add extra line breaks before headings and between sections
    text = re.sub(r'(\n\*.+\*)', r'\n\1', text)
    # Remove stray hashes
    text = re.sub(r'#+', '', text)
    # Remove triple backticks/code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove double spaces
    text = re.sub(r'  +', ' ', text)
    # Clean up multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_send_message(update, "Hello! I am your LLM-powered assistant. Ask me about government services.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task = user_tasks.get(user_id)
    if task and not task.done():     
        task.cancel()
        await safe_send_message(update, "Generation stopped.")
    else:
        await safe_send_message(update, "No active generation to stop.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id
    
    # Send 'typing...' action
    async def keep_typing():
        try:
            while True:
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
                await asyncio.sleep(3)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Error sending chat action: {e}")

    async def stream_and_edit():
        typing_task = asyncio.create_task(keep_typing())
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                async with client.stream("POST", BACKEND_URL, json={"message": user_message}) as response:
                    partial_reply = ""
                    sent_message = await safe_send_message(update, "...")
                    if not sent_message:
                        print("Failed to send initial message")
                        typing_task.cancel()
                        return
                    last_edit_time = time.time()
                    edit_interval = 0.2  # seconds
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
                                # Only edit if enough time has passed
                                if time.time() - last_edit_time > edit_interval:
                                    await safe_edit_message(sent_message, partial_reply, parse_mode=None)
                                    last_edit_time = time.time()
                    # Final edit with complete response, now with Markdown formatting
                    if partial_reply:
                        clean_reply = sanitize_markdown(partial_reply)
                        formatted_reply = format_for_telegram(clean_reply)
                        await safe_edit_message(sent_message, formatted_reply, parse_mode='Markdown')
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Error in stream_and_edit: {e}")
        finally:
            typing_task.cancel()
    
    # Cancel any previous task for this user
    prev_task = user_tasks.get(user_id)
    if prev_task and not prev_task.done():
        prev_task.cancel()
    
    # Start new task
    task = asyncio.create_task(stream_and_edit())
    user_tasks[user_id] = task

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Telegram bot is running...")
    asyncio.run(app.run_polling()) 