# Try/except block to handle import errors more gracefully
try:
    from app import app
except Exception as e:
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error_handler():
        return f"Application initialization error. Please check logs and configuration.", 500