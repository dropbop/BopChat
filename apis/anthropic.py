import os
import anthropic

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
anthropic_client = None  # Default to None

if ANTHROPIC_API_KEY:
    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def anthropic_query(conversation_history):
    """
    Queries the Anthropic API for a non-streaming response.

    Args:
        conversation_history: List of message dictionaries.

    Returns:
        tuple: (assistant_response, error_message) - error_message is None if no error.
    """
    try:
        if not ANTHROPIC_API_KEY or not anthropic_client:
            return None, "Anthropic API key not configured."
            
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=conversation_history
        )
        assistant_response = response.content[0].text
        return assistant_response, None
    except Exception as e:
        return None, str(e)

def anthropic_stream_query(conversation_history):
    """
    Queries the Anthropic API for a streaming response.

    Args:
        conversation_history: List of message dictionaries.

    Yields:
        str: Chunks of the streaming response.
    """
    if not ANTHROPIC_API_KEY or not anthropic_client:
        yield "Anthropic API key not configured."
        return
        
    try:
        with anthropic_client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=conversation_history,
        ) as stream:
            for chunk in stream.text_stream:
                yield chunk
    except Exception as e:
        yield f"\n[Anthropic streaming error: {str(e)}. Falling back...]\n"
        try:
            if anthropic_client:
                response = anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4096,
                    messages=conversation_history,
                )
                yield response.content[0].text
            else:
                yield "Anthropic client not configured properly."
        except Exception as inner_e:
            yield f"\n[Anthropic fallback error: {str(inner_e)}]\n"