from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import os
import json

# Import providers
from providers.anthropic import AnthropicProvider

# Initialize Flask without load_dotenv (Vercel handles env vars)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Load model configurations
try:
    with open('config/models.json') as f:
        MODELS_CONFIG = json.load(f)
except:
    # Fallback for serverless environment
    MODELS_CONFIG = [
        {
            "id": "claude-3-7-sonnet-20250219",
            "name": "Claude 3.7 Sonnet",
            "provider": "anthropic",
            "max_tokens": 4000,
            "description": "Fast, intelligent, and capable of reasoning"
        }
    ]

# Initialize providers
anthropic_provider = AnthropicProvider(api_key=os.environ.get('ANTHROPIC_API_KEY'))

# Simple in-memory message storage until we implement database
chat_history = {}

@app.route('/')
def index():
    return render_template('chat.html', current_year=datetime.now().year)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    chat_id = data.get('chat_id', str(datetime.now().timestamp()))
    model = data.get('model', 'claude-3-7-sonnet-20250219')  # Default to Claude 3.7 Sonnet
    
    # Initialize chat history for this chat if it doesn't exist
    if chat_id not in chat_history:
        chat_history[chat_id] = []
    
    # Add user message to history
    chat_history[chat_id].append({
        'role': 'user',
        'content': message,
        'timestamp': datetime.now().isoformat()
    })
    
    # Get model config
    model_config = next((m for m in MODELS_CONFIG if m['id'] == model), None)
    if not model_config:
        return jsonify({'error': 'Model not found'}), 404
    
    # Route to appropriate provider
    if model_config['provider'] == 'anthropic':
        messages = [{'role': m['role'], 'content': m['content']} for m in chat_history[chat_id]]
        response = anthropic_provider.generate_response(messages, model)
    else:
        return jsonify({'error': 'Provider not supported'}), 400
    
    # Add assistant response to history
    chat_history[chat_id].append({
        'role': 'assistant',
        'content': response,
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({
        'message': response,
        'chat_id': chat_id
    })

@app.route('/history')
def history():
    return render_template('history.html', current_year=datetime.now().year)

@app.route('/settings')
def settings():
    return render_template('settings.html', current_year=datetime.now().year)

@app.route('/login')
def login():
    return render_template('login.html', current_year=datetime.now().year)

# Add handler for Vercel serverless function
from http.server import BaseHTTPRequestHandler

# For local development
if __name__ == '__main__':
    app.run(debug=True)