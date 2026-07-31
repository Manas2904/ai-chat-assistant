# 🤖 AI Chat Assistant

A production-quality AI chat assistant built with Streamlit and Google Gemini API, featuring a modern interface, conversation memory, and robust error handling.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Project Overview

AI Chat Assistant is a sophisticated conversational AI application that provides an intuitive chat interface for interacting with Google's Gemini AI model. The application features a clean, modern UI with real-time responses, conversation history management, and comprehensive error handling. Built with production-ready code practices including type hints, logging, and modular architecture.

## ✨ Features

### Core Functionality
- **Modern Chat Interface**: Clean, responsive UI with sidebar navigation and chat bubbles
- **Markdown Rendering**: Rich text formatting for AI responses including code blocks, tables, and links
- **Typing Indicator**: Visual feedback when AI is processing requests
- **Conversation Memory**: Context-aware responses using full conversation history
- **Clear Chat**: One-click conversation reset functionality

### Technical Excellence
- **Modular Architecture**: Clean separation between UI (`app.py`) and business logic (`backend/llm.py`)
- **Type Safety**: Comprehensive type hints throughout the codebase
- **Error Handling**: Graceful handling of API errors, rate limits, network failures, and invalid input
- **Logging System**: Detailed logging for debugging, monitoring, and auditing
- **Documentation**: Extensive docstrings following Google Python style guide

### User Experience
- **Real-time Statistics**: Live chat metrics in the sidebar
- **API Status Indicator**: Visual confirmation of API key configuration
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Fast Performance**: Optimized for quick response times using Gemini Flash model

## 🛠 Tech Stack

### Frontend
- **Streamlit** (1.28+): Python framework for building web applications
- **Markdown**: Rich text rendering for AI responses

### Backend
- **Google Gemini API** (gemini-2.0-flash-exp): AI model for natural language processing
- **google-genai** (0.3+): Official Google GenAI Python SDK

### Development Tools
- **python-dotenv** (1.0+): Environment variable management
- **Python Logging**: Built-in logging framework
- **Type Hints**: Python type annotations for code clarity

### Infrastructure
- **Docker**: Containerization support for easy deployment
- **Git**: Version control

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google API Key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ai-chat-assistant.git
cd ai-chat-assistant
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Required: Your Google API Key for Gemini AI
# Get your key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_actual_api_key_here
```

### Environment Variable Details

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `GOOGLE_API_KEY` | Yes | Your Google API key for accessing Gemini AI | None |

## 🖼 Screenshots

### Main Chat Interface
```
┌─────────────────────────────────────────────────────────────┐
│  AI Chat Assistant                                    ─ ✕ │
├──────────────┬──────────────────────────────────────────────┤
│              │  Chat                                         │
│  Settings    │  ─────────────────────────────────────────  │
│              │                                               │
│ ✅ API Key   │  👤 User: Hello! Can you help me with...     │
│              │                                               │
│  ┌────────┐  │  🤖 Assistant: Of course! I'd be happy to... │
│  │Clear   │  │                                               │
│  │Chat    │  │  👤 User: How do I create a Python list?     │
│  └────────┘  │                                               │
│              │  🤖 Assistant: You can create a Python list...│
│  Statistics  │                                               │
│  Total: 4    │  ┌────────────────────────────────────────┐  │
│  User: 2     │  │ Type your message here...             │  │
│  AI: 2       │  └────────────────────────────────────────┘  │
│              │                                               │
│ Built with   │                                               │
│ Streamlit    │                                               │
└──────────────┴──────────────────────────────────────────────┘
```

### Sidebar Features
- **API Key Status**: Visual indicator showing if API key is configured
- **Clear Chat Button**: Reset conversation with one click
- **Chat Statistics**: Real-time message counts and user/AI breakdown
- **Brand Info**: Application branding and credits

## 🏗 Project Structure

```
ai-chat-assistant/
├── app.py                 # Streamlit UI application
├── backend/
│   ├── __init__.py       # Backend package initialization
│   └── llm.py            # Gemini API integration module
├── .env                  # Environment variables (not in git)
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── Dockerfile           # Docker container configuration
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## 🚀 Usage

### Starting the Application
```bash
streamlit run app.py
```

### Using the Chat Interface
1. **Type Your Message**: Enter your question or prompt in the chat input
2. **Send Message**: Press Enter or click the send button
3. **View Response**: AI response appears with typing indicator
4. **Continue Conversation**: Maintain context across multiple messages
5. **Clear Chat**: Use the sidebar button to start fresh

### Command Line Options
```bash
# Run on different port
streamlit run app.py --server.port 8501

# Enable file watcher for auto-reload
streamlit run app.py --server.runOnSave true

# Set theme
streamlit run app.py --theme.base dark
```

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t ai-chat-assistant .
```

### Run with Docker
```bash
docker run -p 8501:8501 --env-file .env ai-chat-assistant
```

### Docker Compose (Optional)
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    env_file:
      - .env
    volumes:
      - .:/app
```

Run with:
```bash
docker-compose up
```

## 🔧 Architecture

### UI Layer (`app.py`)
- **Responsibilities**: Streamlit interface, session state, user interactions
- **Key Functions**:
  - `initialize_session_state()`: Session state management
  - `render_sidebar()`: Sidebar UI rendering
  - `render_chat_interface()`: Main chat interface
  - `handle_user_input()`: User input processing

### Backend Layer (`backend/llm.py`)
- **Responsibilities**: API interactions, business logic, error handling
- **Key Components**:
  - `GeminiClient`: Main API client class
  - `Message`: Dataclass for message representation
  - `create_gemini_client()`: Factory function
  - `validate_user_input()`: Input validation

### Data Flow
```
User Input → Streamlit UI → Input Validation → Gemini API → Response Processing → UI Display
```

## 🛡 Error Handling

The application handles various error scenarios gracefully:

| Error Type | Handling | User Message |
|------------|----------|--------------|
| Invalid API Key | Validation at startup | "Configuration Error: Invalid API key" |
| Rate Limits | API error detection | "Rate limit exceeded. Please wait..." |
| Network Issues | Connection error handling | "Network error. Check internet connection" |
| Empty Input | Pre-validation | "Please enter a message" |
| API Errors | Generic error catching | "Error generating response: [details]" |

## 📊 Logging

Logs are configured at INFO level and include:
- **Client Initialization**: API client setup and configuration
- **API Requests**: Request details and conversation context
- **API Responses**: Response generation and processing
- **Error Conditions**: Detailed error information for debugging
- **User Actions**: Chat clearing, message sending, etc.

### Log Format
```
timestamp - logger_name - level - message
```

## 🔮 Future Improvements

### Planned Features
- [ ] **Multi-Model Support**: Add support for other AI models (GPT-4, Claude, etc.)
- [ ] **Conversation Export**: Download chat history as JSON or text files
- [ ] **Custom System Prompts**: Allow users to customize AI behavior
- [ ] **User Authentication**: Add login functionality and user-specific history
- [ ] **Voice Input/Output**: Speech-to-text and text-to-speech capabilities
- [ ] **File Upload**: Support for document analysis and file-based conversations
- [ ] **Streaming Responses**: Real-time streaming of AI responses
- [ ] **Conversation Branching**: Create multiple conversation threads
- [ ] **Dark/Light Theme**: Theme toggle for user preference
- [ ] **Mobile App**: React Native or Flutter mobile application

### Technical Improvements
- [ ] **Unit Tests**: Comprehensive test coverage using pytest
- [ ] **CI/CD Pipeline**: GitHub Actions for automated testing and deployment
- [ ] **Database Integration**: PostgreSQL/MongoDB for persistent conversation storage
- [ ] **Redis Caching**: Cache common responses for improved performance
- [ ] **Rate Limiting**: Implement user-based rate limiting
- [ ] **Monitoring**: Application monitoring with Prometheus/Grafana
- [ ] **Load Balancing**: Support for horizontal scaling
- [ ] **API Rate Limiting**: Backend API rate limiting and quota management

### Documentation
- [ ] **API Documentation**: Complete API reference using Sphinx
- [ ] **Contributing Guide**: Guidelines for contributors
- [ ] **Architecture Diagrams**: Detailed system architecture documentation
- [ ] **Video Tutorials**: Setup and usage video guides

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include docstrings for new functions
- Add tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google AI**: For providing the Gemini API
- **Streamlit**: For the amazing Python web framework
- **Python Community**: For excellent libraries and tools

## 📞 Support

For support, please open an issue in the GitHub repository or contact [your-email@example.com].

## 🔗 Links

- [Google AI Studio](https://makersuite.google.com/app/apikey) - Get your API key
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google GenAI SDK](https://github.com/googleapis/python-genai)
- [Project Repository](https://github.com/yourusername/ai-chat-assistant)

---

**Built with ❤️ using Streamlit and Google Gemini AI**
