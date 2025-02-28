import os

# Store API key but don't initialize client at module level
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

def anthropic_query(conversation_history):
    """
    Queries the Anthropic API for a non-streaming response.

    Args:
        conversation_history: List of message dictionaries.

    Returns:
        tuple: (assistant_response, error_message) - error_message is None if no error.
    """
    try:
        if not ANTHROPIC_API_KEY:
            return None, "Anthropic API key not configured."
            
        # Import and initialize client on demand
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=conversation_history
        )
        assistant_response = response.content[0].text
        return assistant_response, None
    except ImportError:
        return None, "Anthropic package not installed correctly."
    except Exception as e:
        return None, f"Anthropic API error: {str(e)}"

def anthropic_stream_query(conversation_history):
    """
    Queries the Anthropic API for a streaming response.

    Args:
        conversation_history: List of message dictionaries.

    Yields:
        str: Chunks of the streaming response.
    """
    if not ANTHROPIC_API_KEY:
        yield "Anthropic API key not configured."
        return
        
    try:
        # Import and initialize client on demand
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        with client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=conversation_history,
        ) as stream:
            for chunk in stream.text_stream:
                yield chunk
    except ImportError:
        yield "Anthropic package not installed correctly."
    except Exception as e:
        yield f"\n[Anthropic streaming error: {str(e)}]\n"
        yield "Could not complete the request with Anthropic."