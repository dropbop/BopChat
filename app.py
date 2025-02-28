import os
from flask import Flask
from models import init_db
from login import login_bp
from chat import chat_bp # Import chat_bp
from history import history_bp # Import history_bp
from markupsafe import Markup
import markdown

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


# Initialize the database (creates tables if they don’t exist)
init_db()

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(chat_bp) # Register chat_bp
app.register_blueprint(history_bp) # Register history_bp

if __name__ == '__main__':
    app.run(debug=True)