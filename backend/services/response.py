"""
Response generation service using Hugging Face models
"""

import random
import os
import requests
from config import FORMAL_RESPONSES, FUNNY_RESPONSES

# Hugging Face API endpoint
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
        
        # Prepare the prompt
        headers = {"Authorization": f"Bearer {api_key}"}
        
        payload = {
            "inputs": message,
            "parameters": {
                "max_length": 100,
                "temperature": 0.8 if mode == 'funny' else 0.7,
                "top_p": 0.9
            }
        }
        
        # Call Hugging Face API
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                
                # Clean up response
                if generated_text and generated_text != message:
                    # Remove the input from the output if it's included
                    if generated_text.startswith(message):
                        generated_text = generated_text[len(message):].strip()
                    
                    return generated_text if generated_text else get_fallback_response(message, mode)
        
        # If API fails, use fallback
        return get_fallback_response(message, mode)
        
    except Exception as e:
        print(f"⚠️ AI generation error: {e}")
        return get_fallback_response(message, mode)


def get_fallback_response(message, mode):
    """Rule-based fallback responses"""
    message_lower = message.lower()
    
    # Greetings
    if any(word in message_lower for word in ['hi', 'hello', 'hey', 'greetings']):
        return "Hello! How may I assist you today?" if mode == 'formal' else "Hey there! 👋 What's up?"
    
    # How are you
    if 'how are you' in message_lower or "how're you" in message_lower:
        return "I'm functioning well, thank you. How can I help you?" if mode == 'formal' else "I'm doing great! Thanks for asking 😊 What can I do for you?"
    
    # What can you do
    if any(phrase in message_lower for phrase in ['what can you do', 'what do you do', 'help me']):
        return "I'm here to answer your questions and assist with information. Please feel free to ask me anything appropriate." if mode == 'formal' else "I can chat with you about pretty much anything! Ask me questions, and I'll do my best to help out 🤓"
    
    # Thanks
    if any(word in message_lower for word in ['thanks', 'thank you', 'thx']):
        return "You're welcome! Is there anything else I can help you with?" if mode == 'formal' else "You're welcome! Happy to help! 😄"
    
    # Goodbye
    if any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'farewell']):
        return "Goodbye! Have a great day." if mode == 'formal' else "See you later! Take care! 👋"
    
    # Questions about name
    if 'your name' in message_lower or 'who are you' in message_lower:
        return "I'm ChatGuard, an AI assistant designed to provide helpful information." if mode == 'formal' else "I'm ChatGuard! Your friendly neighborhood AI 🤖"
    
    # Default response
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
    # If message is not safe, return canned response
    if classification != 'safe':
        return get_canned_response(classification, mode)
    
    # For safe messages, try to generate AI response
    return generate_ai_response(message, mode)
