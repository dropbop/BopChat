import os
from dotenv import load_dotenv

load_dotenv()

# Flask settings
SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
DEBUG = os.environ.get("FLASK_ENV") == "development"

# Database settings
DATABASE_URL = os.environ.get("DATABASE_URL", 'sqlite:///conversations.db')

# API Keys
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Model configurations
MODEL_NAMES = {
    'anthropic': 'Claude Sonnet 3.6',
    'openai_chatgpt-4o-latest': 'GPT-4o',
    'openai_o3-mini': 'o3-mini',
    'openai_gpt-4.5-preview': 'GPT-4.5',
    'google_gemini-2.0-flash-thinking-exp-01-21': 'Gemini 2.0 FT',
    'google_gemini-2.0-flash-exp': 'Gemini 2.0',
    'google_gemini-exp-1206': 'Gemini 1206',
    'deepseek': 'DeepSeek R1'
}