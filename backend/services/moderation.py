"""
Content moderation service using Hugging Face models
"""

import re
import os
from transformers import pipeline
from config import (
    MODERATION_THRESHOLD,
    OFFENSIVE_PATTERNS,
    SPAM_PATTERNS,
    HUGGINGFACE_MODELS
)

# Initialize toxicity classifier (lazy loading)
_toxicity_classifier = None


def get_toxicity_classifier():
    """Initialize the toxicity classifier on first use"""
    global _toxicity_classifier
    if _toxicity_classifier is None:
        try:
            print("Loading toxicity detection model...")
            _toxicity_classifier = pipeline(
                "text-classification",
                model=HUGGINGFACE_MODELS['toxicity'],
                token=os.getenv('HUGGINGFACE_API_KEY')
            )
            print("✅ Toxicity model loaded")
        except Exception as e:
            print(f"⚠️ Failed to load toxicity model: {e}")
            _toxicity_classifier = False
    return _toxicity_classifier


def is_spam(message):
    """Check if message matches spam patterns"""
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return True
    return False


def has_offensive_patterns(message):
    """Check if message contains offensive patterns"""
    for pattern in OFFENSIVE_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return True
    return False


def check_toxicity_with_hf(message):
    """Use Hugging Face model to detect toxicity"""
    try:
        classifier = get_toxicity_classifier()
        
        if not classifier:
            return {'is_toxic': False, 'score': 0.0}
        
        # Get prediction
        result = classifier(message[:512])[0]  # Limit to 512 chars
        
        # Check if result indicates toxicity
        label = result['label'].lower()
        score = result['score']
        
        is_toxic = 'toxic' in label and score > MODERATION_THRESHOLD
        
        return {
            'is_toxic': is_toxic,
            'score': score if is_toxic else 0.0
        }
        
    except Exception as e:
        print(f"⚠️ Toxicity check error: {e}")
        return {'is_toxic': False, 'score': 0.0}


def moderate_message(message):
    """
    Main moderation function
    
    Returns:
        dict: {
            'classification': 'safe' | 'offensive' | 'irrelevant',
            'confidence': float
        }
    """
    # Check for empty or spam
    if not message or not message.strip() or is_spam(message):
        return {
            'classification': 'irrelevant',
            'confidence': 1.0
        }
    
    # Check offensive patterns
    if has_offensive_patterns(message):
        return {
            'classification': 'offensive',
            'confidence': 0.85
        }
    
    # Check with Hugging Face model
    hf_result = check_toxicity_with_hf(message)
    
    if hf_result['is_toxic']:
        return {
            'classification': 'offensive',
            'confidence': hf_result['score']
        }
    
    # Message is safe
    return {
        'classification': 'safe',
        'confidence': 1.0 - hf_result['score']
    }
