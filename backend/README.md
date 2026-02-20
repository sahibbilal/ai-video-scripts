# Backend API Server

Flask backend for Video Script Generator.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is running:
```bash
ollama serve
```

3. Start the server:
```bash
python app.py
```

Or on Windows:
```bash
run_backend.bat
```

The server will run on http://127.0.0.1:5000

## API Endpoints

- `GET /api/ollama/check` - Check Ollama connection
- `GET /api/ollama/models` - Get available models
- `POST /api/ideas/generate` - Generate video topic ideas
- `POST /api/discuss` - Discuss and refine ideas
- `POST /api/script/generate` - Generate video script
- `POST /api/script/series` - Generate script series

## Troubleshooting

If you get a 500 error:
1. Check that Ollama is running: `ollama list`
2. Check backend logs for detailed error messages
3. Make sure you have at least one model pulled: `ollama pull llama3`
4. Check that all dependencies are installed
