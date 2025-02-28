import anthropic
import os
from typing import List, Dict

class AnthropicProvider:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        
        # Initialize client only when needed to avoid startup errors
        self.client = None
    
    def generate_response(self, messages: List[Dict], model: str = "claude-3-7-sonnet-20250219", max_tokens: int = 4000):
        """
        Generate a response using Anthropic's Claude model.
        
        Args:
            messages: List of message objects with 'role' and 'content'
            model: The Claude model to use
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            The text response from Claude
        """
        try:
            # Initialize client if not already done
            if self.client is None:
                self.client = anthropic.Anthropic(api_key=self.api_key)
                
            # Convert our messages format to Anthropic's format
            # Anthropic expects a list of messages with role and content
            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=messages,
                temperature=0.7
            )
            
            return message.content[0].text
            
        except Exception as e:
            print(f"Error calling Anthropic API: {e}")
            return f"Error generating response: {str(e)}"