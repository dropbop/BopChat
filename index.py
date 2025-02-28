# Try/except block to handle import errors more gracefully
import sys
try:
    from app import app
except Exception as e:
    print(f"Initialization error: {str(e)}", file=sys.stderr)
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error_handler():
        return f"Application initialization error: {str(e)}", 500