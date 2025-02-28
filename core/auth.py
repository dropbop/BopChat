from flask import flash, redirect, url_for, request
from flask_login import UserMixin, login_user as flask_login_user, logout_user as flask_logout_user
from flask_login import LoginManager, login_required

# Create LoginManager instance
login_manager = LoginManager()

# Setup login manager
def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page'
    login_manager.login_message_category = 'error'

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

    @staticmethod
    def get(username):
        users = load_users()
        if username in users:
            return User(username)
        return None
        
    @staticmethod
    def validate(username, password):
        users = load_users()
        if username in users and users[username] == password:
            return True
        return False

def load_users():
    """Load users from users.txt file"""
    users = {}
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                if line.strip():
                    username, password = line.strip().split(':', 1)
                    users[username] = password
    except FileNotFoundError:
        # Create a default admin user if file doesn't exist
        with open('users.txt', 'w') as f:
            f.write('admin:password\n')
        users = {'admin': 'password'}
    return users

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def authenticate_user(username, password):
    """Check if username and password match records"""
    if User.validate(username, password):
        user = User(username)
        flask_login_user(user)
        return True
    return False

# These functions are aliases to maintain compatibility with existing code
login_user = flask_login_user
logout_user = flask_logout_user
# login_required is imported directly from flask_login