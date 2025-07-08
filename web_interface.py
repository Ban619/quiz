from flask import Flask, render_template, request, jsonify, session
import json
import os
from ai_assistant import AIAssistant
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Global AI assistant instance
ai_assistant = None

def initialize_ai():
    """Initialize the AI assistant"""
    global ai_assistant
    try:
        ai_assistant = AIAssistant()
        logger.info("AI Assistant initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize AI Assistant: {e}")
        return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get conversation history from session
        if 'conversation_history' not in session:
            session['conversation_history'] = []
        
        # Generate AI response
        response = ai_assistant.chat(message, session['conversation_history'])
        
        # Update conversation history
        session['conversation_history'].extend([
            f"Human: {message}",
            f"AI: {response}"
        ])
        
        # Limit conversation history to prevent session bloat
        if len(session['conversation_history']) > 20:
            session['conversation_history'] = session['conversation_history'][-20:]
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': 'An error occurred processing your message'}), 500

@app.route('/api/sentiment', methods=['POST'])
def sentiment():
    """Sentiment analysis endpoint"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        result = ai_assistant.analyze_sentiment(text)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Sentiment analysis error: {e}")
        return jsonify({'error': 'An error occurred analyzing sentiment'}), 500

@app.route('/api/generate', methods=['POST'])
def generate():
    """Text generation endpoint"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        max_length = data.get('max_length', 200)
        
        if not prompt:
            return jsonify({'error': 'Prompt cannot be empty'}), 400
        
        generated_text = ai_assistant.generate_text(prompt, max_length)
        
        return jsonify({
            'generated_text': generated_text,
            'prompt': prompt,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Text generation error: {e}")
        return jsonify({'error': 'An error occurred generating text'}), 500

@app.route('/api/batch', methods=['POST'])
def batch_process():
    """Batch processing endpoint"""
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        operation = data.get('operation', 'sentiment')
        
        if not texts:
            return jsonify({'error': 'No texts provided'}), 400
        
        if len(texts) > 10:  # Limit batch size
            return jsonify({'error': 'Maximum 10 texts allowed per batch'}), 400
        
        results = ai_assistant.process_batch(texts, operation)
        
        return jsonify({
            'results': results,
            'operation': operation,
            'count': len(texts),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Batch processing error: {e}")
        return jsonify({'error': 'An error occurred processing batch'}), 500

@app.route('/api/status')
def status():
    """System status endpoint"""
    try:
        model_info = ai_assistant.get_model_info() if ai_assistant else None
        
        return jsonify({
            'status': 'running' if ai_assistant else 'error',
            'model_info': model_info,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return jsonify({'error': 'Status check failed'}), 500

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        session['conversation_history'] = []
        return jsonify({'message': 'Conversation history cleared'})
    except Exception as e:
        logger.error(f"Clear history error: {e}")
        return jsonify({'error': 'Failed to clear history'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Assistant Web Interface...")
    
    # Initialize AI
    if initialize_ai():
        print("✅ AI Assistant loaded successfully!")
        print("🌐 Starting web server...")
        print("📱 Access the interface at: http://localhost:5000")
        print("📋 API endpoints available:")
        print("   - POST /api/chat - Chat with AI")
        print("   - POST /api/sentiment - Analyze sentiment")
        print("   - POST /api/generate - Generate text")
        print("   - POST /api/batch - Batch processing")
        print("   - GET /api/status - System status")
        
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to initialize AI Assistant")
        print("💡 Make sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")