import os
from flask import Flask
from dotenv import load_dotenv
from markupsafe import Markup
import markdown

# Load environment variables from .env file (locally)
if os.path.exists('.env'):
    load_dotenv()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# --- Custom Jinja Filter for Markdown ---
@app.template_filter('markdown')
def markdown_filter(text):
    if text is None:
        return ""
    # Enable extensions like 'extra' for tables, fenced code blocks, and more.
    html = markdown.markdown(text, extensions=['extra', 'sane_lists'])
    return Markup(html)

# Import components after app is created (lazy loading)
# This helps with circular imports and initialization issues
from core.models import init_db
from core.auth import login_bp
from core.chat import chat_bp
from core.history import history_bp

# Initialize the database inside a function that gets called
# This ensures it doesn't run during module import in serverless
@app.before_first_request
def setup():
    init_db()

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(history_bp)

# For local development
if __name__ == '__main__':
    setup()  # Initialize DB for local development
    app.run(debug=os.environ.get("FLASK_ENV") == "development")