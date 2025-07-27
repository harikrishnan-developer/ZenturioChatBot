#!/usr/bin/env python3
"""
Script to manually set Telegram webhook
Usage: python set_webhook.py
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def set_webhook():
    token = os.getenv("TELEGRAM_TOKEN")
    webhook_url = os.getenv("WEBHOOK_URL")
    
    if not token:
        print("❌ TELEGRAM_TOKEN not found in environment variables")
        return False
    
    if not webhook_url:
        print("❌ WEBHOOK_URL not found in environment variables")
        return False
    
    # Telegram API endpoint
    api_url = f"https://api.telegram.org/bot{token}/setWebhook"
    
    # Payload
    payload = {
        "url": webhook_url,
        "drop_pending_updates": True  # Clear any pending updates
    }
    
    print(f"🔄 Setting webhook to: {webhook_url}")
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook set successfully!")
            print(f"📝 Description: {result.get('description', 'N/A')}")
            return True
        else:
            print(f"❌ Failed to set webhook: {result.get('description', 'Unknown error')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def get_webhook_info():
    token = os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        print("❌ TELEGRAM_TOKEN not found in environment variables")
        return
    
    api_url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("ok"):
            webhook_info = result.get("result", {})
            print("\n📊 Current Webhook Info:")
            print(f"   URL: {webhook_info.get('url', 'Not set')}")
            print(f"   Has Custom Certificate: {webhook_info.get('has_custom_certificate', False)}")
            print(f"   Pending Update Count: {webhook_info.get('pending_update_count', 0)}")
            print(f"   Last Error Date: {webhook_info.get('last_error_date', 'None')}")
            print(f"   Last Error Message: {webhook_info.get('last_error_message', 'None')}")
            print(f"   Max Connections: {webhook_info.get('max_connections', 'Default')}")
        else:
            print(f"❌ Failed to get webhook info: {result.get('description', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error getting webhook info: {e}")

def delete_webhook():
    token = os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        print("❌ TELEGRAM_TOKEN not found in environment variables")
        return False
    
    api_url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    
    try:
        response = requests.post(api_url)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook deleted successfully!")
            return True
        else:
            print(f"❌ Failed to delete webhook: {result.get('description', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error deleting webhook: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Telegram Webhook Management Script")
    print("=" * 40)
    
    # Show current webhook info
    get_webhook_info()
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Set webhook")
    print("2. Delete webhook")
    print("3. Get webhook info only")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        set_webhook()
    elif choice == "2":
        delete_webhook()
    elif choice == "3":
        pass  # Already showed info above
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")
    
    # Show final webhook info
    print("\n" + "=" * 40)
    get_webhook_info()