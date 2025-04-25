import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file (when running locally)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    """Renders the main page."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {e}")
        return "An error occurred loading the page. Please check server logs.", 500

@app.route('/login')
def login():
    """Renders the login page."""
    try:
        return render_template('login.html')
    except Exception as e:
        logger.error(f"Error rendering login page: {e}")
        return "An error occurred loading the login page.", 500

@app.route('/chat-history')
def chat_history():
    """Renders the chat history page."""
    try:
        return render_template('chat_history.html')
    except Exception as e:
        logger.error(f"Error rendering chat history page: {e}")
        return "An error occurred loading the chat history page.", 500
        
@app.route('/tests')
def tests():
    """Renders the tests page."""
    try:
        return render_template('tests.html')
    except Exception as e:
        logger.error(f"Error rendering tests page: {e}")
        return "An error occurred loading the tests page.", 500

@app.route('/api/health')
def health_check():
    """Simple endpoint to verify API is working."""
    return jsonify({
        "status": "ok",
        "message": "BopChat API is running"
    })

# This is needed if running locally with `python api/index.py`
if __name__ == '__main__':
    # Make sure debug=False for production environments
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    logger.info(f"Starting Flask app in {'debug' if debug_mode else 'production'} mode")
    app.run(debug=debug_mode, port=5000)