import sys
import traceback

# Try/except block with detailed error reporting
try:
    from minimal_app import app
except Exception as e:
    error_message = f"Application initialization error: {str(e)}"
    error_traceback = traceback.format_exc()
    print(error_message, file=sys.stderr)
    print("\nTraceback:", file=sys.stderr)
    print(error_traceback, file=sys.stderr)
    
    # Create a minimal app that displays the error and traceback
    from flask import Flask, render_template_string
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def error_handler(path):
        error_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
                .error { background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
                .traceback { background-color: #f8f9fa; padding: 15px; border-radius: 4px; font-family: monospace; white-space: pre-wrap; }
                h1 { color: #721c24; }
            </style>
        </head>
        <body>
            <h1>Application Error</h1>
            <div class="error">
                <p><strong>Error:</strong> {{ error }}</p>
            </div>
            <h2>Traceback</h2>
            <div class="traceback">{{ traceback }}</div>
        </body>
        </html>
        """
        return render_template_string(error_template, error=error_message, traceback=error_traceback), 500