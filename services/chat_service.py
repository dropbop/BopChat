"""
Chat service module for BopChat.
Handles message processing, chat history, and communication with providers.
"""
from datetime import datetime
from flask import session
import json

from providers import get_provider_for_model

# Simple in-memory chat history until database is implemented
chat_history = {}

def generate_chat_response(message, model_id, chat_id):
    """
    Generate a response to a chat message using the appropriate provider.
    
    Args:
        message: The user's message text
        model_id: The ID of the model to use
        chat_id: The conversation ID
        
    Returns:
        The generated response text
    """
    # Initialize chat history for this chat if it doesn't exist
    if chat_id not in chat_history:
        chat_history[chat_id] = []
    
    # Add user message to history
    chat_history[chat_id].append({
        'role': 'user',
        'content': message,
        'timestamp': datetime.now().isoformat()
    })
    
    # Get the appropriate provider for this model
    provider = get_provider_for_model(model_id)
    
    # Format messages for the provider
    formatted_messages = [{'role': m['role'], 'content': m['content']} for m in chat_history[chat_id]]
    
    # Get response from provider
    response = provider.generate_response(formatted_messages, model_id)
    
    # Add assistant response to history
    chat_history[chat_id].append({
        'role': 'assistant',
        'content': response,
        'timestamp': datetime.now().isoformat()
    })
    
    return response

def get_user_chat_history(user_id):
    """
    Get all chats for a specific user.
    
    Args:
        user_id: The user's identifier
        
    Returns:
        A list of chat summaries
    """
    # This will be replaced with database queries
    user_chats = []
    
    for chat_id, messages in chat_history.items():
        # In a real implementation, we'd filter by user_id
        # For now, return all chats (this is just a placeholder)
        if messages:
            first_message = messages[0]['content']
            last_message = messages[-1]['content']
            timestamp = messages[-1]['timestamp']
            
            user_chats.append({
                'id': chat_id,
                'title': first_message[:30] + '...' if len(first_message) > 30 else first_message,
                'last_message': last_message[:50] + '...' if len(last_message) > 50 else last_message,
                'timestamp': timestamp
            })
    
    return user_chats

def get_chat_messages(chat_id):
    """
    Get all messages for a specific chat.
    
    Args:
        chat_id: The chat identifier
        
    Returns:
        A list of messages in the chat
    """
    return chat_history.get(chat_id, [])