"""
ChatGuard Bot - Flask Backend
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from services.moderation import moderate_message
from services.response import generate_response

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
PORT = int(os.getenv('FLASK_PORT', 5000))
ENV = os.getenv('FLASK_ENV', 'development')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'ChatGuard Bot API is running',
        'huggingface_configured': bool(os.getenv('HUGGINGFACE_API_KEY'))
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    
    Request body:
        {
            "message": str,
            "mode": "formal" | "funny"
        }
    
    Response:
        {
            "reply": str,
            "classification": str,
            "confidence": float,
            "mode": str
        }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        message = data.get('message', '').strip()
        mode = data.get('mode', 'formal')
        
        # Validate input
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if mode not in ['formal', 'funny']:
            return jsonify({'error': 'Mode must be "formal" or "funny"'}), 400
        
        # Moderate the message
        moderation_result = moderate_message(message)
        classification = moderation_result['classification']
        confidence = moderation_result['confidence']
        
        # Log moderation result
        preview = message[:50] + '...' if len(message) > 50 else message
        print(f'[MODERATION] "{preview}" -> {classification} ({confidence:.1%})')
        
        # Generate response
        reply = generate_response(message, classification, mode)
        
        # Return response
        return jsonify({
            'reply': reply,
            'classification': classification,
            'confidence': round(confidence, 3),
            'mode': mode
        })
        
    except Exception as e:
        print(f'[ERROR] {str(e)}')
        return jsonify({
            'error': 'An error occurred processing your message',
            'details': str(e) if ENV == 'development' else None
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print('\n🚀 ChatGuard Bot Backend')
    print(f'📡 Server: http://localhost:{PORT}')
    print(f'🤗 Hugging Face: {"✅ Configured" if os.getenv("HUGGINGFACE_API_KEY") else "❌ Not configured"}')
    print('\nEndpoints:')
    print('  GET  /api/health')
    print('  POST /api/chat\n')
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=(ENV == 'development')
    )
