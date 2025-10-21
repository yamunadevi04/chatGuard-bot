"""
Configuration constants for ChatGuard Bot
"""

# Moderation settings
MODERATION_THRESHOLD = 0.7  # Toxicity score threshold (0-1)

# Offensive patterns for quick detection
OFFENSIVE_PATTERNS = [
    r'\b(stupid|idiot|dumb|moron|fool)\b',
    r'\b(hate|kill|die|death)\b',
    r'\b(shut\s*up|stfu)\b'
]

# Spam patterns
SPAM_PATTERNS = [
    r'^(.)\1{10,}$',  # Repeated characters
    r'^[^a-zA-Z0-9\s]+$',  # Only special characters
    r'^\s*$'  # Empty or whitespace
]

# Formal mode responses
FORMAL_RESPONSES = {
    'offensive': [
        "I'm here to have respectful conversations. Let's keep things professional.",
        "I appreciate constructive dialogue. Could we rephrase that?",
        "Let's maintain a respectful tone in our conversation.",
        "I'm designed to assist with helpful information. Let's keep our discussion appropriate."
    ],
    'irrelevant': [
        "I didn't quite understand that. Could you please rephrase your question?",
        "That doesn't seem to be a valid query. How may I assist you today?",
        "I'm here to help with meaningful questions. What would you like to know?"
    ]
}

# Funny mode responses
FUNNY_RESPONSES = {
    'offensive': [
        "Whoa there! 🛑 Let's keep it friendly, shall we? 😄",
        "Nice try! But I'm programmed to dodge those kinds of comments 🤖✨",
        "Oops! That triggered my 'nope' detector 🚨 Let's try again!",
        "My sensors are picking up some spicy language 🌶️ Let's cool it down!",
        "Error 404: Inappropriate content not processed 🤓"
    ],
    'irrelevant': [
        "Hmm... my brain.exe has stopped responding to that input 🤔",
        "That sounds like keyboard gymnastics! 🤸 Got a real question?",
        "Beep boop... does not compute 🤖 Try asking me something else!",
        "My AI brain is confused 😵 Want to try a different question?"
    ]
}

# Hugging Face model names
HUGGINGFACE_MODELS = {
    'toxicity': 'unitary/toxic-bert',
    'text_generation': 'microsoft/DialoGPT-medium'
}
