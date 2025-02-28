from flask import Blueprint, render_template, request, jsonify, session, Response, stream_with_context
from app import login_required  # Import directly from app
from apis.openai import openai_query, openai_stream_query
from apis.anthropic import anthropic_query, anthropic_stream_query

chat_bp = Blueprint('chat', __name__)

# In-memory conversation storage (temporary solution)
active_conversations = {}

@chat_bp.route('/')
@login_required
def index():
    return render_template('index.html', conversation_uuid=None, conversation_history=[]) 

@chat_bp.route('/chat/<conversation_uuid>')
@login_required
def chat_conversation(conversation_uuid):
    """
    Route to display a specific conversation by UUID.
    """
    if conversation_uuid not in active_conversations:
        return render_template('error.html', message="Conversation not found.")
        
    conversation = active_conversations[conversation_uuid]
    conversation_history = conversation.get('messages', [])
    model = conversation.get('model', 'anthropic')

    # Model Names Dictionary
    model_names = {
        'anthropic': 'Claude Sonnet 3.6',
        'openai_chatgpt-4o-latest': 'GPT-4o',
        'openai_o3-mini': 'o3-mini',
        'openai_gpt-4.5-preview': 'GPT-4.5',
    }

    return render_template('index.html',
                          conversation_uuid=conversation_uuid,
                          model=model,
                          conversation_history=conversation_history,
                          model_names=model_names)

@chat_bp.route('/new_conversation', methods=['POST'])
@login_required
def new_conversation():
    model = request.form.get('model')
    username = session['username']
    
    # Generate UUID - keep this part
    import uuid
    conversation_uuid = str(uuid.uuid4())
    
    # Store in memory instead of database
    active_conversations[conversation_uuid] = {
        'model': model,
        'username': username,
        'messages': []
    }

    return jsonify({"conversation_uuid": conversation_uuid})

@chat_bp.route('/llm_query', methods=['POST'])
@login_required
def llm_query():
    prompt = request.form.get('prompt')
    selected_model = request.form.get('model', 'anthropic')
    conversation_uuid = request.form.get('conversation_uuid')
    
    if not conversation_uuid:
        return jsonify({"error": "Conversation UUID is missing."}), 400
    
    # Get conversation from memory
    if conversation_uuid not in active_conversations:
        active_conversations[conversation_uuid] = {
            'model': selected_model,
            'username': session['username'],
            'messages': []
        }
    
    conversation = active_conversations[conversation_uuid]
    conversation_history = conversation.get('messages', [])
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

        elif selected_model == 'deepseek':
            assistant_response = "DeepSeek API response placeholder."
        else:
            return jsonify({"error": "Invalid model selected."}), 400

        conversation_history.append({"role": "assistant", "content": assistant_response})
        
        # Update in-memory storage
        conversation['messages'] = conversation_history
        
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
    
    if not conversation_uuid:
        return jsonify({"error": "Conversation UUID is missing."}), 400

    # Get conversation from memory
    if conversation_uuid not in active_conversations:
        active_conversations[conversation_uuid] = {
            'model': selected_model,
            'username': session['username'],
            'messages': []
        }
    
    conversation = active_conversations[conversation_uuid]
    conversation_history = conversation.get('messages', [])
    conversation_history.append({"role": "user", "content": prompt})

    def generate():
        if selected_model.startswith("openai"):
            yield from openai_stream_query(conversation_history, selected_model)
        elif selected_model == 'anthropic':
            yield from anthropic_stream_query(conversation_history)
        elif selected_model == 'deepseek':
            yield "DeepSeek streaming not implemented yet."
        else:
            yield "Streaming not implemented for this model."

    def generate_and_save():
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
            # Save the completed message to in-memory storage
            conversation_history.append({"role": "assistant", "content": assistant_response_content})
            conversation['messages'] = conversation_history

    return Response(stream_with_context(generate_and_save()), mimetype='text/plain')