import os

# Initialize OpenAI client only if needed, with error handling
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = None

# Avoid initializing OpenAI client at module level
# We'll initialize it on demand in the functions

def openai_query(conversation_history, selected_model):
    """
    Queries the OpenAI API for a non-streaming response.

    Args:
        conversation_history: List of message dictionaries.
        selected_model: Model identifier string from the frontend.

    Returns:
        tuple: (assistant_response, error_message) - error_message is None if no error.
    """
    try:
        if not OPENAI_API_KEY:
            return None, "OpenAI API key not configured."
            
        # Initialize OpenAI client on demand
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
            
        if selected_model == "openai_chatgpt-4o-latest":
            openai_model = "chatgpt-4o-latest"
        elif selected_model == "openai_o3-mini":
            openai_model = "o3-mini"
        elif selected_model == "openai_gpt-4.5-preview":
            openai_model = "gpt-4.5-preview"
        else:
            return None, "Invalid OpenAI model selected."

        response = client.chat.completions.create(
            model=openai_model,
            messages=conversation_history,
            max_tokens=4096,
            temperature=0.7,
        )
        assistant_response = response.choices[0].message.content
        return assistant_response, None
    except ImportError:
        return None, "OpenAI package not installed correctly."
    except Exception as e:
        return None, f"OpenAI API error: {str(e)}"

def openai_stream_query(conversation_history, selected_model):
    """
    Queries the OpenAI API for a streaming response.

    Args:
        conversation_history: List of message dictionaries.
        selected_model: Model identifier string from the frontend.

    Yields:
        str: Chunks of the streaming response.
    """
    if not OPENAI_API_KEY:
        yield "OpenAI API key not configured."
        return
        
    try:
        # Initialize OpenAI client on demand
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        if selected_model == "openai_chatgpt-4o-latest":
            openai_model = "chatgpt-4o-latest"
        elif selected_model == "openai_o3-mini":
            openai_model = "o3-mini"
        elif selected_model == "openai_gpt-4.5-preview":
            openai_model = "gpt-4.5-preview"
        else:
            yield "Invalid OpenAI model selected."
            return

        stream = client.chat.completions.create(
            model=openai_model,
            messages=conversation_history,
            max_tokens=1024,
            temperature=0.7,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)
            if content:
                yield content
    except ImportError:
        yield "OpenAI package not installed correctly."
    except Exception as e:
        yield f"\n[OpenAI streaming error: {str(e)}]\n"
        yield "Could not complete the request with OpenAI."