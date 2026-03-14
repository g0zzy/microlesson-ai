# Quick Start Guide - MicroLesson AI

Get up and running in 5 minutes!

## 1. Setup (First Time Only)

```bash
# Get your API key from https://console.anthropic.com/
export ANTHROPIC_API_KEY="your-key-here"

# Install dependencies
pip install -r requirements.txt
```

## 2. Start the App

```bash
# Option A: Use the start script
chmod +x start.sh
./start.sh

# Option B: Manual start
cd backend
python main.py
```

Backend runs at: `http://localhost:8000`

## 3. Open Frontend

```bash
# Option A: Direct open (macOS)
open frontend/index.html

# Option B: With local server
cd frontend
python -m http.server 3000
# Visit http://localhost:3000
```

## 4. Test It

1. Enter topic: "Quantum Computing"
2. Select style: Text
3. Click "Generate Lesson"
4. Wait ~5 seconds
5. Read your lesson!

## Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key not set"
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

### "CORS error"
- Make sure backend is running on port 8000
- Open frontend from same domain or use local server

## API Endpoints

```bash
# Check health
curl http://localhost:8000/health

# Generate lesson
curl -X POST http://localhost:8000/generate-lesson \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI", "style": "text"}'
```

## File Structure

```
microlesson-ai/
├── backend/
│   └── main.py          # FastAPI server
├── frontend/
│   ├── index.html       # UI
│   └── script.js        # Logic
├── requirements.txt     # Python deps
├── README.md           # Full docs
└── start.sh            # Quick start
```

## Next Steps

- Read [README.md](README.md) for full documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) to deploy online
- Check [test_examples.md](test_examples.md) for test topics

## Common Commands

```bash
# Start backend
cd backend && python main.py

# View logs
# (in backend terminal)

# Stop server
# Ctrl+C

# Run with auto-reload
uvicorn backend.main:app --reload
```

## Example Topics

- "How Black Holes Work"
- "JavaScript Promises"
- "The French Revolution"
- "Machine Learning Basics"
- "Climate Change"

---

**Questions?** Check the main README or visit the docs!
