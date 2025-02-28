import os
import json
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session, Response, stream_with_context
from utils import login_required
from models import Conversation, Message, db_session
from apis.openai import openai_query, openai_stream_query
from apis.anthropic import anthropic_query, anthropic_stream_query
from apis.google import google_gemini_query, google_gemini_stream_query

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
@login_required
def index():
    return render_template('index.html', conversation_uuid=None, conversation_history=[]) # Removed model_names here


@chat_bp.route('/chat/<conversation_uuid>')
@login_required
def chat_conversation(conversation_uuid):
    """
    Route to display a specific conversation by UUID.
    Fetches conversation history from the database and renders the chat interface.
    """
    conversation = Conversation.query.filter_by(id=conversation_uuid).first()
    if not conversation:
        return render_template('error.html', message="Conversation not found.")

    messages_db = Message.query.filter_by(conversation_id=conversation_uuid).order_by(Message.timestamp).all()
    conversation_history = [{"role": msg.role, "content": msg.content} for msg in messages_db]

    # --- Model Names Dictionary (Moved INSIDE chat_conversation function) ---
    model_names = {
        'anthropic': 'Claude Sonnet 3.6',
        'openai_chatgpt-4o-latest': 'GPT-4o',
        'openai_o3-mini': 'o3-mini',
        'openai_gpt-4.5-preview': 'GPT-4.5',
        'google_gemini-2.0-flash-thinking-exp-01-21': 'Gemini 2.0 FT',
        'google_gemini-2.0-flash-exp': 'Gemini 2.0',
        'google_gemini-exp-1206': 'Gemini 1206',
        'deepseek': 'DeepSeek R1'
    }

    return render_template('index.html',  # Render index.html
                           conversation_uuid=conversation_uuid,
                           model=conversation.model,
                           conversation_history=conversation_history,
                           model_names=model_names) # Passing model_names here (locally defined)


@chat_bp.route('/new_conversation', methods=['POST'])
@login_required
def new_conversation():
    model = request.form.get('model')
    conversation_uuid = str(uuid.uuid4())
    username = session['username']

    new_conversation_db = Conversation(id=conversation_uuid, username=username, model=model)
    db_session.add(new_conversation_db)
    db_session.commit()

    return jsonify({"conversation_uuid": conversation_uuid})


@chat_bp.route('/llm_query', methods=['POST'])
@login_required
def llm_query():
    prompt = request.form.get('prompt')
    selected_model = request.form.get('model', 'anthropic')
    conversation_uuid = request.form.get('conversation_uuid')
    conversation_history = []

    if not conversation_uuid:
        return jsonify({"error": "Conversation UUID is missing."}), 400

    messages_db = Message.query.filter_by(conversation_id=conversation_uuid).order_by(Message.timestamp).all()
    conversation_history = [{"role": msg.role, "content": msg.content} for msg in messages_db]

    conversation_history.append({"role": "user", "content": prompt})

    try:
        if selected_model.startswith("openai"):
            assistant_response, error_message = openai_query(conversation_history, selected_model)
            if error_message:
                return jsonify({"error": error_message}), 500

        elif selected_model == 'anthropic':
            assistant_response, error_message = anthropic_query(conversation_history)
            if error_message:
                return jsonify({"error": error_message}), 500

        elif selected_model.startswith("google"):
            assistant_response, error_message = google_gemini_query(conversation_history, selected_model)
            if error_message:
                return jsonify({"error": error_message}), 500

        elif selected_model == 'deepseek':
            assistant_response = "DeepSeek API response placeholder."
        else:
            return jsonify({"error": "Invalid model selected."}), 400

        conversation_history.append({"role": "assistant", "content": assistant_response})

        user_message_db = Message(conversation_id=conversation_uuid, role='user', content=prompt)
        assistant_message_db = Message(conversation_id=conversation_uuid, role='assistant', content=assistant_response)
        db_session.add_all([user_message_db, assistant_message_db])
        db_session.commit()


        return jsonify({"response": assistant_response, "conversation_history": conversation_history})
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"error": str(e)}), 500


@chat_bp.route('/llm_query_stream', methods=['POST'])
@login_required
def llm_query_stream():
    prompt = request.form.get('prompt')
    selected_model = request.form.get('model', 'anthropic')
    conversation_uuid = request.form.get('conversation_uuid')
    conversation_history = []

    if not conversation_uuid:
        return jsonify({"error": "Conversation UUID is missing."}), 400

    messages_db = Message.query.filter_by(conversation_id=conversation_uuid).order_by(Message.timestamp).all()
    conversation_history = [{"role": msg.role, "content": msg.content} for msg in messages_db]

    conversation_history.append({"role": "user", "content": prompt})

    def generate():
        if selected_model.startswith("openai"):
            yield from openai_stream_query(conversation_history, selected_model)

        elif selected_model == 'anthropic':
            yield from anthropic_stream_query(conversation_history)

        elif selected_model.startswith("google"):
            yield from google_gemini_stream_query(conversation_history, selected_model)

        elif selected_model == 'deepseek':
            yield "DeepSeek streaming not implemented yet."
        else:
            yield "Streaming not implemented for this model."

    def generate_and_save():
        user_message_db = Message(conversation_id=conversation_uuid, role='user', content=prompt)
        db_session.add(user_message_db)
        db_session.flush()

        assistant_response_content = ""

        try:
            for chunk in generate():
                assistant_response_content += chunk
                yield chunk
        except Exception as e:
            error_message = f"\n[Streaming error: {str(e)}. Partial response saved.]\n"
            assistant_response_content += error_message
            yield error_message
        finally:
            assistant_message_db = Message(conversation_id=conversation_uuid, role='assistant', content=assistant_response_content)
            db_session.add(assistant_message_db)
            db_session.commit()


    return Response(stream_with_context(generate_and_save()), mimetype='text/plain')