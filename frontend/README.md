# Video Script Generator - React Frontend

Professional React-based web interface for the Video Script Generator Bot.

## Features

- Modern, responsive Material-UI design
- Real-time Ollama connection status
- Three-tab workflow: Generate Ideas → Discuss & Refine → Generate Script
- Image description/prompt generation
- Series generation support
- Professional, clean interface

## Installation

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

The app will run on http://localhost:3000

## Building for Production

```bash
npm run build
```

## Backend Setup

Make sure the Flask backend is running on port 5000:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

## Requirements

- Node.js 16+ 
- npm or yarn
- Ollama running locally
- Flask backend running on port 5000
