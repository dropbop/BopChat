from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils import load_users

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            # Redirect to the main chat interface
            return redirect(url_for('chat.index'))
        else:
            flash("Invalid username or password.", "danger")
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out.", "info")
    return redirect(url_for('login.login'))
