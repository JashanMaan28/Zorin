# � ZORIN - Advanced AI Desktop Assistant

<div align="center">

![Zorin Logo](https://img.shields.io/badge/Zorin-AI%20Assistant-00D4AA?style=for-the-badge&logo=robot&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A sophisticated, modern desktop AI assistant with voice interaction, real-time web search, and beautiful animated UI**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Keys](#-api-configuration) • [Contributing](#-contributing)

</div>

---

## 🌟 Overview

Zorin is a cutting-edge AI desktop assistant that combines the power of modern AI models with an intuitive, animated web interface. Built with Python and JavaScript, it offers seamless voice and text interactions, real-time information retrieval, and system integration capabilities.

### 🎯 What Makes Zorin Special

- **🎨 Modern UI**: Beautiful glassmorphism design with animated orb visualizations
- **🎙️ Advanced Voice**: Natural speech recognition and text-to-speech with Edge TTS
- **🧠 Multi-Model AI**: Support for Groq, Cohere, and HuggingFace models
- **🌐 Real-time Search**: Live web search integration for up-to-date information
- **📱 Responsive Design**: Works seamlessly across desktop and mobile browsers
- **🔧 Extensible**: Modular architecture for easy feature additions

---

## ✨ Features

### 🤖 **AI & Conversation**
- Multiple AI model support (Llama 3.3, DeepSeek R1, Gemma 2, etc.)
- Persistent conversation memory with chat history
- Context-aware responses with real-time information
- Custom personality and response styling

### 🎙️ **Voice & Audio**
- Advanced speech recognition with Web Speech API
- Natural text-to-speech using Microsoft Edge TTS
- Voice activation with wake word detection (Pvporcupine)
- Multiple voice options and languages

### 🌐 **Web Integration**
- Real-time web search capabilities
- Live weather updates
- News and information retrieval
- Website content summarization

### 🎨 **User Interface**
- Animated AI orb with multiple states (idle, listening, thinking, speaking)
- Modern glassmorphism design with backdrop blur effects
- Responsive layout for all screen sizes
- Dark theme with cyan/teal accent colors
- Smooth animations and transitions

### � **System Features**
- Real-time system monitoring (CPU, RAM, Network)
- Application launcher integration
- File and folder management capabilities
- Cross-platform compatibility (Windows, macOS, Linux)

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **Modern web browser** (Chrome, Firefox, Edge, Safari)
- **Microphone** for voice input (optional)
- **Internet connection** for AI models and web search

### 1. Clone the Repository

```bash
git clone https://github.com/JashanMaan28/Zorin.git
cd Zorin
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv env-zorin
env-zorin\Scripts\activate

# macOS/Linux
python3 -m venv env-zorin
source env-zorin/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
# User Configuration
Username=YourName

# AI Model Configuration
Model=llama-3.3-70b-versatile
GroqAPIKey=your_groq_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
HuggingFaceAPIKey=your_huggingface_api_key_here

# Voice Configuration
pvporcupine_ACCESS_KEY=your_picovoice_api_key_here
```

### 5. Run the Application

```bash
python run.py
```

The application will automatically open in your default web browser at `http://localhost:8000`

---

## 🔑 API Configuration

### Required API Keys

| Service | Purpose | Free Tier | Get Key |
|---------|---------|-----------|---------|
| **Groq** | Primary AI model | ✅ Yes | [groq.com](https://groq.com) |
| **Cohere** | Web search & embeddings | ✅ Yes | [cohere.ai](https://cohere.ai) |
| **HuggingFace** | Alternative AI models | ✅ Yes | [huggingface.co](https://huggingface.co) |
| **Picovoice** | Wake word detection | ✅ Limited | [picovoice.ai](https://picovoice.ai) |

### Setting Up API Keys

1. **Groq (Primary AI)**:
   - Sign up at [groq.com](https://groq.com)
   - Navigate to API Keys section
   - Create new API key
   - Add to `.env` file

2. **Cohere (Web Search)**:
   - Register at [cohere.ai](https://cohere.ai)
   - Go to Dashboard → API Keys
   - Generate new key
   - Add to `.env` file

3. **HuggingFace (Optional)**:
   - Create account at [huggingface.co](https://huggingface.co)
   - Go to Settings → Access Tokens
   - Create new token
   - Add to `.env` file

4. **Picovoice (Wake Word)**:
   - Sign up at [picovoice.ai](https://picovoice.ai)
   - Access Console → Porcupine
   - Copy access key
   - Add to `.env` file

---

## 🎮 Usage

### Basic Interaction

1. **Text Input**: Type your question in the input field and press Enter or click Send
2. **Voice Input**: Click the microphone button and speak your question
3. **Settings**: Click the gear icon to configure API keys and models
4. **Chat History**: Click the chat icon to view conversation history

### Voice Commands

- **"Hey Zorin"** - Wake word activation (if configured)
- **Natural conversation** - Ask questions, request information, get help
- **System commands** - "Open calculator", "Check weather", etc.

### Keyboard Shortcuts

- **Ctrl + Enter** - Send message
- **Cmd/Ctrl + J** - Activate voice input
- **Escape** - Return to main interface

### Advanced Features

#### Model Selection
Choose from multiple AI models in settings:
- **Llama 3.3 70B** (Recommended) - Balanced performance and accuracy
- **DeepSeek R1** - Advanced reasoning capabilities  
- **Gemma 2 9B** - Fast and efficient responses

#### Web Search Integration
Zorin automatically searches the web for current information when needed:
```
User: "What's the weather in Tokyo today?"
Zorin: *searches web* "Currently in Tokyo, it's 22°C with partly cloudy skies..."
```

#### Chat Management
- **Auto-save**: Conversations are automatically saved
- **Archive**: Old chats are archived by date
- **Export**: Download chat history as JSON

---

## 🏗️ Project Structure

```
Zorin/
├── 📁 backend/              # Python backend modules
│   ├── ChatBot.py          # Main AI chat logic
│   ├── Model.py            # AI model management
│   ├── RealtimeSearchEngine.py  # Web search functionality
│   ├── speechToText.py     # Voice recognition
│   ├── textToSpeech.py     # Voice synthesis
│   ├── commands.py         # System commands
│   ├── features.py         # Core features
│   └── settings.py         # Configuration management
├── 📁 frontend/             # Web interface
│   ├── index.html          # Main UI
│   ├── style.css           # Modern styling
│   ├── main.js             # Core JavaScript
│   ├── controller.js       # Backend communication
│   └── 📁 assets/          # Static assets
├── � Data/                 # User data and logs
│   ├── ChatLog.json        # Current conversation
│   └── 📁 Files/           # Generated content
├── 📁 chatlog_archives/     # Historical conversations
├── main.py                 # Core application logic
├── run.py                  # Application launcher
├── requirements.txt        # Python dependencies
└── .env                    # Environment configuration
```

---

## � Development

### Architecture

Zorin uses a hybrid architecture combining:

- **Backend**: Python with Eel for web app integration
- **Frontend**: Modern web technologies (HTML5, CSS3, ES6+)
- **Communication**: Eel framework for Python-JavaScript bridge
- **AI**: Multiple model providers via REST APIs
- **Voice**: Web Speech API + Edge TTS integration

### Key Components

#### Backend (Python)
- **ChatBot.py**: Manages AI conversations and context
- **Model.py**: Handles multiple AI model integrations
- **RealtimeSearchEngine.py**: Web search and information retrieval
- **speechToText.py**: Voice input processing
- **textToSpeech.py**: Voice output generation

#### Frontend (JavaScript)
- **OrbController**: Manages visual AI orb animations
- **WebSocket Communication**: Real-time backend interaction
- **Responsive UI**: Modern glassmorphism design
- **State Management**: Handles conversation and UI states

### Adding New Features

1. **Backend Features**: Add to `/backend/` directory
2. **UI Components**: Modify `/frontend/` files
3. **API Integration**: Update `Model.py` and settings
4. **Commands**: Extend `commands.py` for system integration

---

## 🎨 Customization

### Themes & Styling

The UI uses CSS custom properties for easy theming:

```css
:root {
  --primary-color: #0ab0d1;
  --secondary-color: #05738a;
  --accent-color: #29e9dd;
  --background-color: rgba(25, 25, 25, 0.95);
  --text-color: #ffffff;
}
```

### Voice Configuration

Customize voice settings in `.env`:

```env
# Voice Settings
VOICE_LANGUAGE=en-US
VOICE_SPEED=1.0
VOICE_PITCH=1.0
TTS_PROVIDER=edge
```

### AI Personality

Modify the system prompt in `backend/ChatBot.py`:

```python
System = f"""
You are Zorin, a helpful AI assistant.
Customize personality traits here...
"""
```

---

## 🚀 Deployment

### Local Network Access

To access Zorin from other devices on your network:

1. Find your local IP address
2. Update `run.py` to bind to `0.0.0.0`
3. Access via `http://YOUR_IP:8000`

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "run.py"]
```

---

## 🔮 Roadmap

### Upcoming Features

- [ ] � **Media Control**: Spotify, YouTube Music integration
- [ ] 📁 **File Management**: Advanced file operations and search
- [ ] 🔍 **Screen OCR**: Text extraction from screen content
- [ ] � **Auto Startup**: System tray integration
- [ ] 📧 **Email Integration**: Read and compose emails
- [ ] 🎨 **Theme Engine**: Light/dark mode with custom themes
- [ ] 🤖 **Plugin System**: Third-party extension support
- [ ] 🌐 **Cloud Sync**: Cross-device conversation sync
- [ ] 📱 **Mobile App**: Native mobile companion
- [ ] 🧠 **Memory System**: Long-term conversation memory

### Version History

- **v2.0.0** - Modern UI redesign with orb animations
- **v1.5.0** - Multi-model AI support and web search
- **v1.0.0** - Initial release with basic chat functionality

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Getting Started

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines

- **Code Style**: Follow PEP 8 for Python, ESLint for JavaScript
- **Documentation**: Update README and code comments
- **Testing**: Add tests for new features
- **Issues**: Use GitHub issues for bug reports and feature requests

### Areas for Contribution

- 🐛 **Bug Fixes**: Help improve stability
- 🎨 **UI/UX**: Enhance the user interface
- 🔧 **Features**: Add new functionality
- 📚 **Documentation**: Improve guides and tutorials
- 🌍 **Localization**: Add language support

---

## 📋 Troubleshooting

### Common Issues

#### Installation Problems

**Issue**: `pip install` fails with permission errors
```bash
# Solution: Use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Issue**: Microphone not working
```bash
# Check microphone permissions in browser
# Ensure HTTPS or localhost for Web Speech API
```

#### Runtime Errors

**Issue**: "Module not found" errors
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

**Issue**: API key errors
```bash
# Verify .env file exists and contains valid keys
# Check API key permissions and quotas
```

### Getting Help

- 📖 **Documentation**: Check this README first
- 🐛 **Bug Reports**: Use GitHub Issues
- 💬 **Discussions**: GitHub Discussions for questions
- 📧 **Contact**: [jashanpreetsingh.tech](https://jashanpreetsingh.tech)

---

## � License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

- **Eel**: Apache 2.0 License
- **Bootstrap Icons**: MIT License
- **Groq SDK**: Apache 2.0 License
- **Edge TTS**: MIT License

---

## 🙏 Acknowledgments

- **Microsoft** for Edge TTS integration
- **Groq** for high-performance AI inference
- **Cohere** for web search capabilities
- **Bootstrap** for UI components
- **The open-source community** for inspiration and tools

---

## 📬 Contact & Support

<div align="center">

**Made with ❤️ by [Jashanpreet Singh](https://jashanpreetsingh.tech)**

[![Website](https://img.shields.io/badge/Website-jashanpreetsingh.tech-blue?style=for-the-badge)](https://jashanpreetsingh.tech)
[![GitHub](https://img.shields.io/badge/GitHub-JashanMaan28-black?style=for-the-badge&logo=github)](https://github.com/JashanMaan28)

**Star ⭐ this repository if you found it helpful!**

</div>

---

<div align="center">
<sub>Built with Python 🐍, JavaScript ⚡, and lots of ☕</sub>
</div>
