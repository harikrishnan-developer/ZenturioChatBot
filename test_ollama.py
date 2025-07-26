#!/usr/bin/env python3
"""
Test script to verify Ollama is running and Qwen:1.8b is available
"""

import requests
import json

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    try:
        # Test basic connection
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible")
            return True
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Make sure it's running on localhost:11434")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return False

def test_qwen_model():
    """Test if Qwen:1.8b model is available"""
    try:
        # Check available models
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            qwen_models = [model for model in models if 'qwen' in model['name'].lower()]
            
            if qwen_models:
                print("✅ Qwen models found:")
                for model in qwen_models:
                    print(f"   - {model['name']} (size: {model.get('size', 'unknown')})")
                return True
            else:
                print("❌ No Qwen models found. You may need to pull the model:")
                print("   ollama pull qwen:1.8b")
                return False
        else:
            print(f"❌ Failed to get model list: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False

def test_qwen_generation():
    """Test if Qwen:1.8b can generate responses"""
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "qwen:1.8b",
            "prompt": "Hello, can you help me with government services?",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 100
            }
        }
        
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get('response', '').strip()
            if generated_text:
                print("✅ Qwen:1.8b is working correctly!")
                print(f"Sample response: {generated_text[:100]}...")
                return True
            else:
                print("❌ Qwen:1.8b returned empty response")
                return False
        else:
            print(f"❌ Failed to generate response: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing generation: {e}")
        return False

def main():
    print("🔍 Testing Ollama and Qwen:1.8b integration...\n")
    
    # Test 1: Connection
    if not test_ollama_connection():
        print("\n💡 To start Ollama:")
        print("   1. Install Ollama from https://ollama.ai")
        print("   2. Run: ollama serve")
        print("   3. Run: ollama pull qwen:1.8b")
        return
    
    print()
    
    # Test 2: Model availability
    if not test_qwen_model():
        print("\n💡 To install Qwen:1.8b:")
        print("   ollama pull qwen:1.8b")
        return
    
    print()
    
    # Test 3: Generation
    if test_qwen_generation():
        print("\n🎉 All tests passed! Your LLM fallback should work correctly.")
        print("\nNext steps:")
        print("1. Restart your Rasa action server")
        print("2. Test the bot with questions it doesn't know")
        print("3. The bot will use Qwen:1.8b as fallback")
    else:
        print("\n❌ Generation test failed. Check your Ollama setup.")

if __name__ == "__main__":
    main() 