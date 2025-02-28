import sys

# Try/except block to handle import errors more gracefully
try:
    from app import app
except Exception as e:
    error_message = f"Application initialization error: {str(e)}"
    print(error_message, file=sys.stderr)
    
    # Create a minimal app that displays the error
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
                h1 { color: #721c24; }
                code { background: #f8f9fa; padding: 2px 5px; border-radius: 3px; font-family: monospace; }
            </style>
        </head>
        <body>
            <h1>Application Error</h1>
            <div class="error">
                <p>The application could not start properly.</p>
                <p><strong>Error:</strong> {{ error }}</p>
            </div>
            <p>Please check the application logs for more detailed information.</p>
        </body>
        </html>
        """
        return render_template_string(error_template, error=error_message), 500