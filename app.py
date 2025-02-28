import os
from flask import Flask
from dotenv import load_dotenv
from markupsafe import Markup
import markdown

# Load environment variables from .env file
load_dotenv()

# Import components from their new locations
from core.models import init_db
from core.auth import login_bp  # Assuming login.py was renamed to auth.py but blueprint name is the same
from core.chat import chat_bp
from core.history import history_bp

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


# Initialize the database (creates tables if they don't exist)
init_db()

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(history_bp)

if __name__ == '__main__':
    app.run(debug=os.environ.get("FLASK_ENV") == "development")