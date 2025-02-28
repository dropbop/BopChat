import os
from flask import Flask, render_template_string

# Create a minimal Flask application for troubleshooting
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default-dev-key")

@app.route('/')
def hello():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Troubleshooting App</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .card { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <h1>Troubleshooting App</h1>
        <div class="card">
            <p>If you can see this page, basic Flask routing is working!</p>
            <p>Your Vercel deployment is functioning correctly.</p>
        </div>
    </body>
    </html>
    """)

# Debug configuration
app.debug = True

# Required for Vercel
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))