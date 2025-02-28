import os
from flask import Flask

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Import components after app is created
from core.models import init_db
from core.auth import login_bp
from core.chat import chat_bp
from core.history import history_bp

# Initialize database on first request
@app.before_first_request
def setup():
    init_db()

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(history_bp)

# This is important for Vercel deployment
app.debug = False