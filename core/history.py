from flask import Blueprint, render_template, session
from core.utils import login_required
from core.models import Conversation

history_bp = Blueprint('history', __name__)

@history_bp.route('/history')
@login_required
def history():
    # Get conversations for the logged-in user, newest first, ordered by start_timestamp.
    conversations = Conversation.query.filter_by(username=session['username']).order_by(Conversation.start_timestamp.desc()).all() # Changed to start_timestamp
    return render_template('history.html', conversations=conversations)