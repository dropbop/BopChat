import os
from functools import wraps
from flask import session, redirect, url_for, flash

def load_users():
    users = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    users_path = os.path.join(base_dir, 'users.txt')
    try:
        with open(users_path, 'r') as f:
            for line in f:
                if ':' in line:
                    username, password = line.strip().split(':', 1)
                    users[username] = password
    except FileNotFoundError:
        print("users.txt not found. Create it with username:password lines.")
    return users

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function
