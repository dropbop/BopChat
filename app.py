import os
import sys
import traceback
from flask import Flask, redirect, url_for, flash, session
from functools import wraps

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default-secret-key-for-development")

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function

# Load users function
def load_users():
    # For now, embedded credentials directly
    return {"jack": "water"}

# Import and register blueprints with detailed error handling
try:
    from core.auth import login_bp
    app.register_blueprint(login_bp)
    print("Successfully registered login blueprint", file=sys.stderr)
except Exception as e:
    error_msg = f"Error registering login blueprint: {str(e)}"
    tb = traceback.format_exc()
    print(error_msg, file=sys.stderr)
    print(tb, file=sys.stderr)
    
    # Create a minimal login blueprint
    from flask import Blueprint, render_template, request
    login_bp = Blueprint('login', __name__)
    
    @login_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username == "jack" and password == "water":
                session['username'] = username
                return redirect(url_for('root'))
            else:
                flash("Invalid username or password.", "danger")
        return render_template('login.html')
    
    @login_bp.route('/logout')
    def logout():
        session.pop('username', None)
        flash("Logged out.", "info")
        return redirect(url_for('login.login'))
    
    app.register_blueprint(login_bp)

try:
    from core.chat import chat_bp
    app.register_blueprint(chat_bp)
    print("Successfully registered chat blueprint", file=sys.stderr)
except Exception as e:
    error_msg = f"Error registering chat blueprint: {str(e)}"
    tb = traceback.format_exc()
    print(error_msg, file=sys.stderr)
    print(tb, file=sys.stderr)
    
    # Create a minimal chat blueprint
    from flask import Blueprint, render_template_string
    chat_bp = Blueprint('chat', __name__)
    
    @chat_bp.route('/chat')
    @login_required
    def index():
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chat - Recovery Mode</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
                .card { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <h1>Chat Interface - Recovery Mode</h1>
            <div class="card">
                <p>The chat blueprint could not be loaded properly.</p>
                <p>Check the server logs for detailed error information.</p>
            </div>
            <a href="{{ url_for('login.logout') }}">Logout</a>
        </body>
        </html>
        """)
    
    app.register_blueprint(chat_bp)

# Root route - redirect to login or chat based on authentication
@app.route('/')
def root():
    if 'username' in session:
        return redirect(url_for('chat.index'))
    return redirect(url_for('login.login'))

# Debug configuration
app.debug = os.environ.get("DEBUG", "False").lower() == "true"

# Required for Vercel
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))