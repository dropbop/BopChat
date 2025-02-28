import os
from flask import Flask, redirect, url_for, flash
from functools import wraps
from flask import session, redirect, url_for, flash

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default-secret-key-for-development")

# Login required decorator - moved here to prevent circular imports
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function

# Load users function - moved here to prevent circular imports
def load_users():
    # For now, embedded credentials directly
    return {"jack": "water"}

# Import components after defining necessary functions
from core.auth import login_bp
from core.chat import chat_bp

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(chat_bp)

# Root route - redirect to login
@app.route('/')
def root():
    return redirect(url_for('login.login'))

# This is important for Vercel deployment
app.debug = os.environ.get("DEBUG", "False").lower() == "true"

# Required for Vercel
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))