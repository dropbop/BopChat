# BopChat

A simple, self-hosted chat interface for accessing LLM APIs with your own API keys.

## Project Overview

BopChat allows you to host a ChatGPT-like interface that uses your own API keys to communicate with various large language models (LLMs). Perfect for sharing access with friends without sharing your actual API keys.

### Features (Planned)

- **Multi-Model Support**: Access different LLMs through a unified interface
- **User Authentication**: Simple login system for sharing with friends
- **Conversation History**: Keep track of your chats
- **User Settings**: Configure model parameters like temperature and max tokens
- **Clean UI**: Intuitive chat interface similar to commercial offerings

## Tech Stack

- **Backend**: Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Deployment**: Vercel (serverless)

## Project Structure

```
bopchat/
├── app.py                       # Main application entry point
├── routes/
│   ├── __init__.py              # Route initialization
│   ├── chat.py                  # Chat functionality routes
│   ├── history.py               # Conversation history routes
│   ├── login.py                 # Authentication routes
│   └── settings.py              # User settings routes
├── config/
│   └── models.json              # Available models configuration
├── providers/
│   ├── __init__.py              # Provider factory/router
│   ├── anthropic.py             # Anthropic API integration
│   └── openai.py                # OpenAI API integration (future)
├── services/
│   ├── chat_service.py          # Chat logic
│   ├── auth_service.py          # Authentication logic
│   └── user_service.py          # User management
├── database/
│   ├── __init__.py
│   ├── models.py                # SQLAlchemy models
│   └── db.py                    # Database connection handling
├── static/
│   ├── css/
│   │   └── style.css            # Main stylesheet
│   ├── js/
│   │   ├── chat.js              # Chat interface functionality
│   │   └── settings.js          # Settings interface functionality
│   └── img/
│       └── favicon.ico          # Site favicon
├── templates/
│   ├── base.html                # Base template with header/footer
│   ├── chat.html                # Chat interface
│   ├── history.html             # Chat history view
│   ├── login.html               # Login page
│   └── settings.html            # User settings
├── utils/
│   ├── auth.py                  # Authentication helpers
│   └── helpers.py               # Generic helper functions
├── requirements.txt             # Project dependencies
└── vercel.json                  # Vercel deployment configuration
```

## Development Roadmap

### Phase 1: Core Functionality
- [x] Project setup
- [ ] Modular Flask app structure
- [ ] Anthropic provider integration
- [ ] Simple chat interface
- [ ] Basic API handling

### Phase 2: User Management
- [ ] User authentication
- [ ] Admin controls for account creation
- [ ] User-specific settings
- [ ] Conversation history storage

### Phase 3: Model Expansion
- [ ] OpenAI provider integration
- [ ] Model parameter customization
- [ ] Additional LLM providers as needed

### Phase 4: Polish & Deployment
- [ ] UI refinements
- [ ] Mobile responsiveness
- [ ] Error handling and rate limiting
- [ ] Vercel deployment optimization

## Getting Started

### Prerequisites
- Python 3.9+
- API keys for supported LLM providers

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/bopchat.git
   cd bopchat
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables
   ```
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. Run the application
   ```
   flask run
   ```

## Contributing

This is a personal project but suggestions are welcome. Feel free to open an issue to discuss any ideas.

## License

This project is licensed under the MIT License - see the LICENSE file for details.