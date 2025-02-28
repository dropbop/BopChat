from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/<path:path>')
def catch_all(path):
    return f"You requested: {path}"

if __name__ == '__main__':
    app.run(debug=True)