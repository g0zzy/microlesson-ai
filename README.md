# MicroLesson AI

> Learn anything in 5 minutes with AI-powered personalized lessons

MicroLesson AI is a hackathon-ready web app that generates personalized 5-minute lessons on any topic using Claude AI. Choose your learning style (text, voice, or visual) and get instant, structured content.

## Features

- **AI-Powered Content**: Uses Claude API to generate high-quality educational content
- **3 Learning Styles**:
  - 📖 **Text**: Read a well-structured article
  - 🎧 **Voice**: Listen to audio narration using browser TTS
  - 📊 **Visual**: Navigate through 5 interactive slides
- **Fixed Structure**: Every lesson has Introduction → 3 Key Concepts → Summary
- **Browser-Based**: No installations needed, runs entirely in the browser
- **Fast**: Generates lessons in ~5-10 seconds

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Claude API**: AI content generation (Sonnet 4.5)
- **Pydantic**: Data validation

### Frontend
- **Vanilla HTML/CSS/JavaScript**: No framework dependencies
- **Web Speech API**: Browser-native text-to-speech
- **Responsive Design**: Works on desktop and mobile

## Project Structure

```
microlesson-ai/
├── backend/
│   └── main.py              # FastAPI server with Claude integration
├── frontend/
│   ├── index.html           # UI and styling
│   └── script.js            # Frontend logic and API calls
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Quick Start

### Prerequisites

- Python 3.9+
- Anthropic API Key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone or download the project**
   ```bash
   cd microlesson-ai
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root:
   ```bash
   ANTHROPIC_API_KEY=your_api_key_here
   ```

   Or export directly:
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

4. **Start the backend server**
   ```bash
   cd backend
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

5. **Open the frontend**

   Simply open `frontend/index.html` in your browser, or serve it with a local server:
   ```bash
   cd frontend
   python -m http.server 3000
   ```

   Then visit `http://localhost:3000`

## Usage

1. **Enter a topic** you want to learn (e.g., "Quantum Computing", "Photosynthesis")
2. **Select your learning style**: Text, Voice, or Visual
3. **Click "Generate Lesson"**
4. **Consume the content**:
   - Text: Read the article
   - Voice: Click play to hear the lesson (includes transcript)
   - Visual: Navigate through slides with arrow keys or buttons

## Example Topics

Try these topics to test the app:

- **Science**: "How Black Holes Work", "DNA Replication", "Climate Change"
- **Technology**: "Blockchain Basics", "Machine Learning", "Quantum Computing"
- **History**: "The Renaissance", "World War II", "Ancient Egypt"
- **Skills**: "Public Speaking", "Time Management", "Critical Thinking"
- **Programming**: "JavaScript Closures", "React Hooks", "API Design"

## API Documentation

### Endpoints

#### `POST /generate-lesson`

Generate a personalized lesson.

**Request:**
```json
{
  "topic": "Quantum Computing",
  "style": "text"
}
```

**Response (Text):**
```json
{
  "type": "text",
  "content": "Introduction to Quantum Computing\n\n..."
}
```

**Response (Voice):**
```json
{
  "type": "voice",
  "content": "Welcome to this lesson on quantum computing..."
}
```

**Response (Visual):**
```json
{
  "type": "slides",
  "slides": [
    {
      "title": "Introduction: Quantum Computing",
      "text": "Quantum computing is a revolutionary technology..."
    },
    ...
  ]
}
```

#### `GET /health`

Check API health and configuration.

**Response:**
```json
{
  "status": "healthy",
  "api_key_configured": true,
  "message": "Ready to generate lessons"
}
```

## How It Works

### Content Generation Pipeline

1. **User Input**: Topic + Learning Style
2. **Prompt Engineering**: Custom prompts for each style
3. **Claude API Call**: Generate structured content
4. **Response Formatting**: Parse and validate response
5. **Frontend Rendering**: Display in chosen format

### Prompt Strategy

The backend uses specialized prompts for each learning style:

- **Text**: Structured article with headers and paragraphs
- **Voice**: Conversational tone optimized for TTS
- **Visual**: JSON array of exactly 5 slides with titles and text

### Text-to-Speech

The voice feature uses the **Web Speech API** (`SpeechSynthesis`), which is built into modern browsers. No additional API keys needed!

## Deployment

### Deploy Backend (Multiple Options)

#### Option 1: Render.com
1. Create a new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `ANTHROPIC_API_KEY`

#### Option 2: Railway.app
1. Create new project from GitHub
2. Add `ANTHROPIC_API_KEY` environment variable
3. Railway auto-detects Python and runs the app

#### Option 3: Fly.io
1. Install flyctl
2. Run `fly launch` in project directory
3. Set secret: `fly secrets set ANTHROPIC_API_KEY=your_key`
4. Deploy: `fly deploy`

### Deploy Frontend

#### Option 1: Netlify/Vercel
1. Drag and drop the `frontend` folder
2. Update `API_URL` in `script.js` to your backend URL

#### Option 2: GitHub Pages
1. Push frontend folder to GitHub
2. Enable GitHub Pages in settings
3. Update `API_URL` in `script.js`

## Customization

### Adjust Lesson Length

In `backend/main.py`, modify the prompt:
```python
Total length: 300-500 words for a 5-minute read/listen.
```

Change to `500-800 words` for longer lessons.

### Change AI Model

In `backend/main.py`, line 96:
```python
model="claude-sonnet-4-5-20250929",  # Latest Claude model
```

Options:
- `claude-opus-4-5-20251101` (more powerful, slower)
- `claude-haiku-4-20250514` (faster, cheaper)

### Customize Voice

In `frontend/script.js`, line 202:
```javascript
currentUtterance.rate = 0.9;  // Speed (0.5 to 2.0)
currentUtterance.pitch = 1.0; // Pitch (0 to 2)
```

### Add More Slides

In `backend/main.py`, change from 5 to N slides in the visual prompt.

## Troubleshooting

### Backend won't start
- Check if API key is set: `echo $ANTHROPIC_API_KEY`
- Verify port 8000 is available: `lsof -i :8000`

### CORS errors
- Make sure backend is running on port 8000
- Check `allow_origins` in `main.py` (line 21)

### Voice not playing
- Use Chrome, Edge, or Safari (best TTS support)
- Check browser console for errors
- Ensure speaker volume is up

### Claude API errors
- Verify API key is valid at console.anthropic.com
- Check if you have credits remaining
- Review API rate limits

## Performance

- **Lesson generation**: ~3-8 seconds
- **API cost**: ~$0.01-0.03 per lesson (using Sonnet)
- **Bundle size**: <10KB (no frameworks!)

## Future Enhancements

- [ ] Quiz generation after lessons
- [ ] Save/bookmark lessons
- [ ] Multi-language support
- [ ] PDF export
- [ ] Progress tracking
- [ ] Custom lesson length slider
- [ ] Premium voices (ElevenLabs, OpenAI TTS)

## License

MIT License - feel free to use this for your hackathon!

## Credits

Built with:
- [Claude API](https://www.anthropic.com/claude) by Anthropic
- [FastAPI](https://fastapi.tiangolo.com/)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

---

**Made for hackathons** - Build time: ~2 hours
