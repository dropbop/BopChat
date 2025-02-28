from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, logout_user, current_user
from core.login import login_bp, load_users, user_loader_callback

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'  # route for login page

# Pre-load users from the file (adjust path as needed)
users = load_users('users.txt')

@login_manager.user_loader
def load_user(user_id):
    return user_loader_callback(user_id, users)

# Register blueprint from core/login.py
app.register_blueprint(login_bp)

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))

if __name__ == '__main__':
    app.run(debug=True)
