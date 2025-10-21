import random
import os
import requests
from config import FORMAL_RESPONSES, FUNNY_RESPONSES

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"


def get_canned_response(classification, mode):
    responses = FORMAL_RESPONSES if mode == 'formal' else FUNNY_RESPONSES
    return random.choice(responses[classification])


def generate_ai_response(msg, mode):
    try:
        key = os.getenv('HUGGINGFACE_API_KEY')
        
        if not key or key == 'hf_your_token_here':
            print("⚠️ No valid Hugging Face API key, using fallback")
            return get_fallback_response(msg, mode)
    
        headers = {"Authorization": f"Bearer {key}"}
        
        data = {
            "inputs": msg,
            "parameters": {
                "max_length": 100,
                "temperature": 0.8 if mode == 'funny' else 0.7,
                "top_p": 0.9
            }
        }
        
        # call API
        response = requests.post(API_URL, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get('generated_text', '')
                
                if text and text != msg:
                    if text.startswith(msg):
                        text = text[len(msg):].strip()
                    
                    return text if text else get_fallback_response(msg, mode)
        
        return get_fallback_response(msg, mode)
        
    except Exception as e:
        print(f"⚠️ AI generation error: {e}")
        return get_fallback_response(msg, mode)


def get_fallback_response(msg, mode):
    msg_lower = msg.lower()

    # greetings
    if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'greetings']):
        return "Hello! How may I assist you today?" if mode == 'formal' else "Hey there! 👋 What's up?"

    # how are you
    if 'how are you' in msg_lower or "how're you" in msg_lower:
        return "I'm functioning well, thank you. How can I help you?" if mode == 'formal' else "I'm doing great! Thanks for asking 😊 What can I do for you?"
 
    # what can you do
    if any(phrase in msg_lower for phrase in ['what can you do', 'what do you do', 'help me']):
        return "I'm here to answer your questions and assist with information. Please feel free to ask me anything appropriate." if mode == 'formal' else "I can chat with you about pretty much anything! Ask me questions, and I'll do my best to help out 🤓"
    
    # thanks
    if any(word in msg_lower for word in ['thanks', 'thank you', 'thx']):
        return "You're welcome! Is there anything else I can help you with?" if mode == 'formal' else "You're welcome! Happy to help! 😄"
    
    # goodbye
    if any(word in msg_lower for word in ['bye', 'goodbye', 'see you', 'farewell']):
        return "Goodbye! Have a great day." if mode == 'formal' else "See you later! Take care! 👋"
    
    # name
    if 'your name' in msg_lower or 'who are you' in msg_lower:
        return "I'm ChatGuard, an AI assistant designed to provide helpful information." if mode == 'formal' else "I'm ChatGuard! Your friendly neighborhood AI 🤖"

    # default
    return "I understand your question. Could you provide more details so I can give you a better answer?" if mode == 'formal' else "Interesting question! 🤔 Can you tell me more about what you're looking for?"


def generate_response(msg, classification, mode='formal'):
    # if not safe, use predefined responses
    if classification != 'safe':
        return get_canned_response(classification, mode)

    # otherwise generate AI response
    return generate_ai_response(msg, mode)

import random
import os
import requests
from config import FORMAL_RESPONSES, FUNNY_RESPONSES

HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"


def get_canned_response(classification, mode):
    """Get pre-defined response for offensive/irrelevant content"""
    responses = FORMAL_RESPONSES if mode == 'formal' else FUNNY_RESPONSES
    return random.choice(responses[classification])


def generate_ai_response(message, mode):
    """Generate AI response using Hugging Face API"""
    try:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        
        if not api_key or api_key == 'hf_your_token_here':
            print("⚠️ No valid Hugging Face API key, using fallback")
            return get_fallback_response(message, mode)
    
        headers = {"Authorization": f"Bearer {api_key}"}
        
        payload = {
            "inputs": message,
            "parameters": {
                "max_length": 100,
                "temperature": 0.8 if mode == 'funny' else 0.7,
                "top_p": 0.9
            }
        }
        
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')         
                if generated_text and generated_text != message:
                    if generated_text.startswith(message):
                        generated_text = generated_text[len(message):].strip()
                    
                    return generated_text if generated_text else get_fallback_response(message, mode)
        
        return get_fallback_response(message, mode)
        
    except Exception as e:
        print(f"⚠️ AI generation error: {e}")
        return get_fallback_response(message, mode)


def get_fallback_response(message, mode):
    """Rule-based fallback responses"""
    message_lower = message.lower()

    if any(word in message_lower for word in ['hi', 'hello', 'hey', 'greetings']):
        return "Hello! How may I assist you today?" if mode == 'formal' else "Hey there! 👋 What's up?"

    if 'how are you' in message_lower or "how're you" in message_lower:
        return "I'm functioning well, thank you. How can I help you?" if mode == 'formal' else "I'm doing great! Thanks for asking 😊 What can I do for you?"
 
    if any(phrase in message_lower for phrase in ['what can you do', 'what do you do', 'help me']):
        return "I'm here to answer your questions and assist with information. Please feel free to ask me anything appropriate." if mode == 'formal' else "I can chat with you about pretty much anything! Ask me questions, and I'll do my best to help out 🤓"
    
    if any(word in message_lower for word in ['thanks', 'thank you', 'thx']):
        return "You're welcome! Is there anything else I can help you with?" if mode == 'formal' else "You're welcome! Happy to help! 😄"
    
    if any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'farewell']):
        return "Goodbye! Have a great day." if mode == 'formal' else "See you later! Take care! 👋"
    
    if 'your name' in message_lower or 'who are you' in message_lower:
        return "I'm ChatGuard, an AI assistant designed to provide helpful information." if mode == 'formal' else "I'm ChatGuard! Your friendly neighborhood AI 🤖"

    return "I understand your question. Could you provide more details so I can give you a better answer?" if mode == 'formal' else "Interesting question! 🤔 Can you tell me more about what you're looking for?"


def generate_response(message, classification, mode='formal'):
    """
    Main response generation function
    
    Args:
        message: User's message
        classification: 'safe', 'offensive', or 'irrelevant'
        mode: 'formal' or 'funny'
    
    Returns:
        str: Generated response
    """
    if classification != 'safe':
        return get_canned_response(classification, mode)

    return generate_ai_response(message, mode)
