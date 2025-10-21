import re
import os
from transformers import pipeline
from config import (
    MODERATION_THRESHOLD,
    OFFENSIVE_PATTERNS,
    SPAM_PATTERNS,
    HUGGINGFACE_MODELS
)

toxicity_model = None


def get_toxicity_classifier():
    global toxicity_model
    if toxicity_model is None:
        try:
            print("Loading toxicity detection model...")
            toxicity_model = pipeline(
                "text-classification",
                model=HUGGINGFACE_MODELS['toxicity'],
                token=os.getenv('HUGGINGFACE_API_KEY')
            )
            print("✅ Toxicity model loaded")
        except Exception as e:
            print(f"⚠️ Failed to load toxicity model: {e}")
            toxicity_model = False
    return toxicity_model


def is_spam(msg):
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, msg, re.IGNORECASE):
            return True
    return False


def has_offensive_patterns(msg):
    for pattern in OFFENSIVE_PATTERNS:
        if re.search(pattern, msg, re.IGNORECASE):
            return True
    return False


def check_toxicity_with_hf(msg):
    try:
        model = get_toxicity_classifier()
        
        if not model:
            return {'is_toxic': False, 'score': 0.0}
        
        result = model(msg[:512])[0]
        
        label = result['label'].lower()
        score = result['score']
        
        toxic = 'toxic' in label and score > MODERATION_THRESHOLD
        
        return {
            'is_toxic': toxic,
            'score': score if toxic else 0.0
        }
        
    except Exception as e:
        print(f"⚠️ Toxicity check error: {e}")
        return {'is_toxic': False, 'score': 0.0}


def moderate_message(msg):
    # check for empty or spam
    if not msg or not msg.strip() or is_spam(msg):
        return {
            'classification': 'irrelevant',
            'confidence': 1.0
        }
    
    # check offensive patterns
    if has_offensive_patterns(msg):
        return {
            'classification': 'offensive',
            'confidence': 0.85
        }
    
    # check with model
    result = check_toxicity_with_hf(msg)
    
    if result['is_toxic']:
        return {
            'classification': 'offensive',
            'confidence': result['score']
        }
    
    # message is safe
    return {
        'classification': 'safe',
        'confidence': 1.0 - result['score']
    }
