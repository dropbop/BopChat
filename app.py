from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({
        "status": "success",
        "message": "Flask is now working on Vercel!"
    })

@app.route('/test')
def test():
    return jsonify({
        "test": "This is a test endpoint"
    })

# This is important for Vercel deployment
app.debug = False

# No if __name__ == '__main__' block needed for Vercel