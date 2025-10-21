import random
import os
import requests
from config import FORMAL_RESPONSES, FUNNY_RESPONSES

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def get_canned_response(classification, mode):
    responses = FORMAL_RESPONSES if mode == 'formal' else FUNNY_RESPONSES
    return random.choice(responses[classification])

def generate_ai_response(msg, mode):
    try:
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key and groq_key != 'your_groq_api_key_here':
            return generate_groq_response(msg, mode, groq_key)
        return get_fallback_response(msg, mode)
        
    except Exception as e:
        print(f"AI generation error: {e}")
        return get_fallback_response(msg, mode)


def generate_groq_response(msg, mode, api_key):
    """Generate response using Groq API (fast and free)"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = (
            "You are a helpful and friendly AI assistant. Keep responses concise and appropriate."
            if mode == 'formal' else
            "You are a fun and friendly AI assistant. Be casual, use emojis, and keep it lighthearted!"
        )
        
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": msg}
            ],
            "temperature": 0.8 if mode == 'funny' else 0.7,
            "max_tokens": 150
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            text = result['choices'][0]['message']['content']
            print(f"Response: {text[:100]}")
            return text
        else:
            print(f"Error: {response.text[:200]}")
            return get_fallback_response(msg, mode)
            
    except Exception as e:
        print(f"Error: {e}")
        return get_fallback_response(msg, mode)


def get_fallback_response(msg, mode):
    msg_lower = msg.lower()
    if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'greetings']):
        return "Hello! How may I assist you today?" if mode == 'formal' else "Hey there! 👋 What's up?"
    if 'how are you' in msg_lower or "how're you" in msg_lower:
        return "I'm functioning well, thank you. How can I help you?" if mode == 'formal' else "I'm doing great! Thanks for asking 😊 What can I do for you?"
    if any(phrase in msg_lower for phrase in ['what can you do', 'what do you do', 'help me']):
        return "I'm here to answer your questions and assist with information. Please feel free to ask me anything appropriate." if mode == 'formal' else "I can chat with you about pretty much anything! Ask me questions, and I'll do my best to help out 🤓"
    if any(word in msg_lower for word in ['thanks', 'thank you', 'thx']):
        return "You're welcome! Is there anything else I can help you with?" if mode == 'formal' else "You're welcome! Happy to help! 😄"
    if any(word in msg_lower for word in ['bye', 'goodbye', 'see you', 'farewell']):
        return "Goodbye! Have a great day." if mode == 'formal' else "See you later! Take care! 👋"
    if 'your name' in msg_lower or 'who are you' in msg_lower:
        return "I'm ChatGuard, an AI assistant designed to provide helpful information." if mode == 'formal' else "I'm ChatGuard! Your friendly neighborhood AI 🤖"
    return "I understand your question. Could you provide more details so I can give you a better answer?" if mode == 'formal' else "Interesting question! 🤔 Can you tell me more about what you're looking for?"


def generate_response(msg, classification, mode='formal'):
    if classification != 'safe':
        return get_canned_response(classification, mode)
    return generate_ai_response(msg, mode)
