# Video Script Generator Bot

A professional web application for generating video scripts using Ollama AI models. Generate trending topic ideas, discuss and refine them, and create structured scripts optimized for video recording with support for multiple languages, image descriptions, and series generation.

## 🚀 Features

### Core Features
- **Idea Generation**: AI-powered suggestions for trending video topics (AI, WordPress, Robotics, General Tech, or Any category)
- **Discussion & Refinement**: Interactive chat interface to refine ideas with AI before script generation
- **Script Generation**: Create detailed, structured video scripts optimized for recording
- **Series Generation**: Generate multiple interconnected scripts (episodes) from a single idea
- **Multi-Language Support**: Generate scripts in English, Urdu, Hindi, Spanish, French, Arabic, Chinese, and more
- **Image Integration**: Include image descriptions and AI image prompts within scripts
- **Character Count Tracking**: Automatic calculation based on slow speaking pace (600 chars/min)
- **Professional UI**: Modern React frontend with Material-UI design
- **Ollama Integration**: Works with any Ollama model locally (no API keys needed)

### Script Features
- **Structured Format**: Hook, Introduction, Key Points, Conclusion, and Call-to-Action
- **Beginner-Friendly**: Simple paragraph format for easy reading during recording
- **Customizable**: Adjust video length, tone (Professional/Casual/Educational), and keywords
- **Image Cues**: Optional visual descriptions and AI image generation prompts
- **Save to Files**: Export scripts as plain text files with timestamps

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download from python.org](https://www.python.org)
  - ⚠️ **Important**: Check "Add Python to PATH" during installation
- **Node.js 16+** - [Download from nodejs.org](https://nodejs.org)
- **Ollama** - [Download from ollama.com](https://ollama.com)
  - Must be installed and running
  - At least one model pulled (e.g., `ollama pull llama3`)

## 🏗️ Architecture

- **Frontend**: React + Material-UI (Vite)
- **Backend**: Flask REST API
- **AI Engine**: Ollama local models
- **Shared Modules**: Python modules in `src/` directory

## 🚀 Quick Start (Recommended)

The easiest way to get started is using the automated startup script:

### Windows

1. **Double-click `start.bat`** in the project root directory

The script will:
- ✅ Check for Python, Node.js, and Ollama
- ✅ Create virtual environments if needed
- ✅ Install all dependencies automatically
- ✅ Start both backend and frontend servers
- ✅ Open the application in your browser

The application will be available at: **http://localhost:3000**

### What the Script Does

1. Verifies Python installation (tries `python`, `python3`, `py`)
2. Checks Node.js installation
3. Verifies Ollama is running
4. Creates/activates backend virtual environment
5. Installs backend dependencies (`flask`, `flask-cors`, `ollama`)
6. Installs frontend dependencies (React, Material-UI, etc.)
7. Starts Flask backend on port 5000
8. Starts React frontend on port 3000
9. Opens browser automatically

## 📦 Manual Installation

If you prefer to set up manually or the automated script doesn't work:

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python app.py
```

Backend will run on **http://localhost:5000**

### Step 2: Frontend Setup

Open a **new terminal window**:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on **http://localhost:3000**

### Step 3: Start Ollama

Make sure Ollama is running:

```bash
# Start Ollama server (if not already running)
ollama serve

# Pull a model if you haven't already
ollama pull llama3
# or
ollama pull mistral
# or any other model you prefer
```

## 📖 Usage Guide

### Workflow

The application follows a three-step workflow:

#### 1. Generate Ideas (Tab 1)
- Select an Ollama model from the dropdown
- Choose a topic category (AI, WordPress, Robotics, General Tech, or Any)
- Click "Generate Ideas" to get trending topic suggestions
- Click on any idea to select it and proceed to discussion

#### 2. Discuss & Refine (Tab 2)
- Review the selected idea
- Select an Ollama model (if different from step 1)
- Ask questions or request refinements in the input field
- Click "Discuss" to get AI responses
- Continue the conversation to refine your idea
- Click "Finalize Idea & Generate Script" when ready

#### 3. Generate Script (Tab 3)
- Review the finalized idea
- Select an Ollama model
- **Optional**: Enter a custom topic (overrides finalized idea if provided)
- Set video length in minutes (1-10 minutes)
- Choose script language (English, Urdu, Hindi, Spanish, French, Arabic, Chinese, etc.)
- Choose tone/style (Professional, Casual, Educational)
- **Optional**: Add additional keywords/points
- **Optional**: Enable "Include image descriptions and visual cues"
  - Choose image type: Descriptions, AI Prompts, or Both
- **Optional**: Generate a series
  - Enter number of episodes (1-10)
  - Each episode builds on previous ones
- Click "Generate Script" or "Generate Series"
- Review the generated script
- Copy or save the script manually

### Character Count Calculation

- **Speaking pace**: Slow (120 words/minute = ~600 characters/minute)
- **1-minute video**: ~600 characters
- The app automatically calculates target character count based on video length

### Script Format

Generated scripts include:
- **Hook**: Attention-grabbing opening
- **Paragraphs**: Simple, readable content for recording
- **Visual Cues**: Image descriptions or AI prompts (if enabled)
- **Call-to-Action**: Engaging conclusion

## 📁 Project Structure

```
ai-videos/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── venv/              # Virtual environment (created automatically)
│   └── README.md          # Backend-specific docs
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── IdeaGenerator.jsx
│   │   │   ├── DiscussionTab.jsx
│   │   │   └── ScriptGenerator.jsx
│   │   ├── services/
│   │   │   └── api.js     # API service layer
│   │   ├── App.jsx        # Main React component
│   │   └── main.jsx       # Entry point
│   ├── package.json       # Node.js dependencies
│   ├── vite.config.js     # Vite configuration
│   └── README.md          # Frontend-specific docs
├── src/                    # Shared Python modules
│   ├── ai_client.py       # Ollama integration
│   ├── idea_generator.py  # Idea generation logic
│   ├── script_generator.py # Script generation logic
│   ├── script_formatter.py # Script formatting
│   ├── utils.py           # Utility functions
│   └── main.py            # Original Tkinter GUI (legacy)
├── output/                 # Generated scripts (created automatically)
├── start.bat              # Automated startup script (Windows)
├── requirements.txt       # Legacy Python dependencies
├── run.py                 # Legacy Tkinter runner
└── README.md             # This file
```

## 🔌 API Endpoints

The Flask backend provides the following REST API endpoints:

### Ollama Management
- `GET /api/ollama/check` - Check if Ollama is connected
- `GET /api/ollama/models` - Get list of available Ollama models

### Idea Generation
- `POST /api/ideas/generate` - Generate trending topic ideas
  ```json
  {
    "category": "AI",
    "model": "llama3"
  }
  ```

### Discussion
- `POST /api/discuss` - Discuss and refine ideas
  ```json
  {
    "idea": "Your idea here",
    "question": "Your question",
    "conversationHistory": [],
    "model": "llama3"
  }
  ```

### Script Generation
- `POST /api/script/generate` - Generate a single script
  ```json
  {
    "idea": "Your finalized idea",
    "topic": "Optional custom topic",
    "videoLength": 1,
    "tone": "Professional",
    "keywords": "optional keywords",
    "model": "llama3",
    "language": "English",
    "includeImages": true,
    "imageType": "both"
  }
  ```

- `POST /api/script/series` - Generate a script series
  ```json
  {
    "idea": "Your finalized idea",
    "numEpisodes": 3,
    "videoLength": 1,
    "tone": "Professional",
    "keywords": "optional keywords",
    "model": "llama3",
    "language": "English",
    "includeImages": true,
    "imageType": "both"
  }
  ```

## 🐛 Troubleshooting

### Python Not Found
**Error**: `[ERROR] Python is not installed or not in PATH`

**Solutions**:
1. Install Python from [python.org](https://www.python.org)
   - ⚠️ **Check "Add Python to PATH" during installation**
   - Restart your computer after installation
2. If Python is already installed, add it to PATH:
   - Search for "Environment Variables" in Windows
   - Edit "Path" variable
   - Add Python installation folder (e.g., `C:\Python39`)
   - Add Python Scripts folder (e.g., `C:\Python39\Scripts`)
   - Restart command prompt
3. Use Python Launcher: Install Python from Microsoft Store or with "py launcher" option

### Ollama Not Connected
**Error**: `Ollama is not connected` or `Ollama Not Connected` status

**Solutions**:
1. Start Ollama server:
   ```bash
   ollama serve
   ```
2. Verify Ollama is running:
   ```bash
   ollama list
   ```
3. Check Ollama is accessible at `http://localhost:11434`
4. Make sure Ollama is installed from [ollama.com](https://ollama.com)

### No Models Available
**Error**: `No Ollama models found` or `model 'llama3' not found`

**Solutions**:
1. Pull a model:
   ```bash
   ollama pull llama3
   # or
   ollama pull mistral
   ```
2. Verify models are available:
   ```bash
   ollama list
   ```
3. Click "Refresh Models" in the application

### Script Generation Fails
**Error**: `500 INTERNAL SERVER ERROR` or `Failed to generate script`

**Solutions**:
1. Check backend terminal for detailed error messages
2. Ensure you have finalized an idea in the Discussion tab
3. Verify the selected model is available
4. Check that Ollama is running and accessible
5. For non-English languages, wait longer (up to 5 minutes) - generation takes more time

### Timeout Errors
**Error**: `timeout of 300000ms exceeded`

**Solutions**:
1. This is normal for non-English languages (Urdu, Hindi, etc.) - generation takes longer
2. Wait for the process to complete (up to 5 minutes)
3. Ensure Ollama has enough resources (RAM, CPU)
4. Try a smaller model if available

### Frontend Build Errors
**Error**: `crypto$2.getRandomValues is not a function`

**Solution**: This should be fixed in the current version. If it occurs:
1. Delete `node_modules` folder in `frontend/`
2. Delete `package-lock.json` in `frontend/`
3. Run `npm install` again

### Backend Dependencies Issues
**Error**: `Failed to install backend dependencies`

**Solutions**:
1. Make sure virtual environment is activated
2. Upgrade pip: `python -m pip install --upgrade pip`
3. Install dependencies manually:
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

### Port Already in Use
**Error**: `Address already in use` or port conflict

**Solutions**:
1. Close other applications using ports 3000 or 5000
2. Kill processes using these ports:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```
3. Change ports in `backend/app.py` and `frontend/vite.config.js` if needed

## 🔧 Configuration

### Ollama Settings
- **Default Host**: `http://localhost:11434`
- **Configurable**: Can be changed in `src/ai_client.py`
- **No API Keys**: All processing is local

### Speaking Pace
- **Default**: Slow (600 characters/minute)
- **Configurable**: Can be adjusted in `src/utils.py`

### Timeouts
- **Frontend API**: 5 minutes (300 seconds) for long operations
- **Backend**: Handles timeouts gracefully with user-friendly messages

## 📝 Development

### Running in Development Mode

**Backend**:
```bash
cd backend
venv\Scripts\activate  # Windows
python app.py
```

**Frontend**:
```bash
cd frontend
npm run dev
```

### Building for Production

**Frontend**:
```bash
cd frontend
npm run build
```

Built files will be in `frontend/dist/`

## 📚 Legacy Tkinter GUI

The project originally included a Tkinter GUI (`src/main.py`). While the React frontend is now the primary interface, the Tkinter version is still available:

```bash
python -m src.main
# or
python run.py
```

## 🔗 Git Repository

Repository: `git@github-bilal:sahibbilal/ai-video-scripts.git`

To clone:
```bash
git clone git@github-bilal:sahibbilal/ai-video-scripts.git
cd ai-video-scripts
```

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section above
2. Review backend/frontend logs for detailed error messages
3. Ensure all prerequisites are installed and configured correctly

---

**Made with ❤️ for content creators**
