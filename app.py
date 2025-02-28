import os
from flask import Flask, redirect, url_for

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default-secret-key-for-development")

# Import components after app is created
from core.models import init_db
from core.auth import login_bp
from core.chat import chat_bp
from core.history import history_bp

# Initialize database once on startup
with app.app_context():
    init_db()

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(history_bp)

# Root route - redirect to login
@app.route('/')
def root():
    return redirect(url_for('login.login'))

# This is important for Vercel deployment
app.debug = False