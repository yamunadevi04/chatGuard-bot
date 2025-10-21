import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from services.moderation import moderate_message
from services.response import generate_response

load_dotenv()

app = Flask(__name__)
CORS(app)

PORT = int(os.getenv('FLASK_PORT', 5000))
ENV = os.getenv('FLASK_ENV', 'development')


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'ChatGuard Bot API is running',
        'huggingface_configured': bool(os.getenv('HUGGINGFACE_API_KEY'))
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # getting data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        msg = data.get('message', '').strip()
        mode = data.get('mode', 'formal')
        
        if not msg:
            return jsonify({'error': 'Message is required'}), 400
        
        if mode not in ['formal', 'funny']:
            return jsonify({'error': 'Mode must be "formal" or "funny"'}), 400
        # checking the message: moderate message
        result = moderate_message(msg)
        classification = result['classification']
        confidence = result['confidence']
        preview = msg[:50] + '...' if len(msg) > 50 else msg
        print(f'[MODERATION] "{preview}" -> {classification} ({confidence:.1%})')
        reply = generate_response(msg, classification, mode)
        # send back response
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
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
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
