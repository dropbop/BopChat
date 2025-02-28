import os
import anthropic

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
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
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=conversation_history,
        )
        yield response.content[0].text