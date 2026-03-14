"""
MicroLesson AI - FastAPI Backend
Generates personalized 5-minute lessons using Claude API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
import os
from typing import Literal
import json
<<<<<<< Updated upstream
import base64
from urllib import error, request as urllib_request

load_dotenv()
=======
import requests
import base64
>>>>>>> Stashed changes

app = FastAPI(title="MicroLesson AI API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Claude client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


class LessonRequest(BaseModel):
    """Request model for lesson generation"""
    topic: str
    style: Literal["text", "voice", "visual"]


class TextResponse(BaseModel):
    """Response model for text lessons"""
    type: str
    content: str


class SlideContent(BaseModel):
    """Individual slide content"""
    title: str
    text: str


class VisualResponse(BaseModel):
    """Response model for visual lessons"""
    type: str
    slides: list[SlideContent]


class VoiceResponse(BaseModel):
    """Response model for voice lessons"""
    type: str
    content: str
    audio_base64: str
    mime_type: str


def generate_lesson_prompt(topic: str, style: str) -> str:
    """
    Generate the Claude prompt based on topic and learning style

    Args:
        topic: The subject to teach
        style: Learning style (text, voice, or visual)

    Returns:
        Formatted prompt for Claude
    """

    base_requirements = f"""Create a 5-minute educational lesson about: {topic}

The lesson MUST follow this exact structure:
1. Introduction (engaging hook and overview)
2. Key Concept 1 (main idea with explanation)
3. Key Concept 2 (main idea with explanation)
4. Key Concept 3 (main idea with explanation)
5. Summary (recap and takeaway)

Total length: 300-500 words for a 5-minute read/listen.
Use clear, concise language suitable for quick learning."""

    if style == "text":
        return f"""{base_requirements}

Format as a well-structured article with clear section headers.
Make it engaging and easy to read."""

    elif style == "voice":
        return f"""{base_requirements}

Format for AUDIO narration:
- Use conversational tone
- Short, clear sentences
- Natural pauses (use punctuation)
- No special characters or formatting
- Speak directly to the listener"""

    elif style == "visual":
        return f"""{base_requirements}

Format as EXACTLY 5 SLIDES in JSON format with image prompts:
[
  {{
    "title": "Introduction: [Topic]",
    "text": "Hook + overview (2-3 sentences)",
    "image_prompt": "A simple, educational illustration representing [topic introduction]"
  }},
  {{
    "title": "Key Concept 1: [Name]",
    "text": "Explanation (2-3 sentences)",
    "image_prompt": "Visual representation of [concept 1]"
  }},
  {{
    "title": "Key Concept 2: [Name]",
    "text": "Explanation (2-3 sentences)",
    "image_prompt": "Visual representation of [concept 2]"
  }},
  {{
    "title": "Key Concept 3: [Name]",
    "text": "Explanation (2-3 sentences)",
    "image_prompt": "Visual representation of [concept 3]"
  }},
  {{
    "title": "Summary & Takeaway",
    "text": "Recap + key message (2-3 sentences)",
    "image_prompt": "Summary visualization of [topic]"
  }}
]

IMPORTANT: Each image_prompt should be a clear, concise description (5-10 words) for AI image generation.
Return ONLY valid JSON array, no other text."""

    return base_requirements


def generate_image_hf(prompt: str) -> str:
    """
    Generate image using Hugging Face Inference API

    Args:
        prompt: Text description for image generation

    Returns:
        Base64 encoded image string
    """
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    hf_token = os.getenv("HUGGINGFACE_API_KEY")

    # If no HF token, return a placeholder
    if not hf_token:
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2Y1ZjdmYSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiM2NjdlZWEiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5JbWFnZSBQbGFjZWhvbGRlcjwvdGV4dD48L3N2Zz4="

    headers = {"Authorization": f"Bearer {hf_token}"}

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=30
        )

        if response.status_code == 200:
            # Convert image bytes to base64
            image_bytes = response.content
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            return f"data:image/png;base64,{base64_image}"
        else:
            # Return placeholder on error
            return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2Y1ZjdmYSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiM2NjdlZWEiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5JbWFnZSBVbmF2YWlsYWJsZTwvdGV4dD48L3N2Zz4="
    except Exception as e:
        print(f"Image generation error: {e}")
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2Y1ZjdmYSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiM2NjdlZWEiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5JbWFnZSBFcnJvcjwvdGV4dD48L3N2Zz4="


def call_claude_api(prompt: str) -> str:
    """
    Call Claude API to generate lesson content

    Args:
        prompt: The formatted prompt

    Returns:
        Generated content from Claude
    """
    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",  # Latest Claude model
            max_tokens=1500,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Claude API error: {str(e)}"
        )


def synthesize_speech(text: str) -> tuple[str, str]:
    """
    Convert lesson text into speech using the ElevenLabs API.

    Args:
        text: Narration text to synthesize

    Returns:
        Tuple of base64-encoded audio data and MIME type
    """
    if not ELEVENLABS_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="ELEVENLABS_API_KEY not set"
        )

    endpoint = (
        f"https://api.elevenlabs.io/v1/text-to-speech/"
        f"{ELEVENLABS_VOICE_ID}?output_format=mp3_44100_128"
    )
    payload = json.dumps({
        "text": text,
        "model_id": ELEVENLABS_MODEL_ID,
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.8
        }
    }).encode("utf-8")

    req = urllib_request.Request(
        endpoint,
        data=payload,
        headers={
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        },
        method="POST"
    )

    try:
        with urllib_request.urlopen(req) as response:
            audio_bytes = response.read()
            mime_type = response.headers.get_content_type() or "audio/mpeg"
            audio_base64 = base64.b64encode(audio_bytes).decode("ascii")
            return audio_base64, mime_type
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise HTTPException(
            status_code=500,
            detail=f"ElevenLabs API error: {detail or exc.reason}"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"ElevenLabs API error: {str(exc)}"
        )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MicroLesson AI API",
        "version": "1.0.0"
    }


@app.post("/generate-lesson")
async def generate_lesson(request: LessonRequest):
    """
    Generate a personalized lesson based on topic and learning style

    Args:
        request: LessonRequest with topic and style

    Returns:
        Lesson content formatted for the chosen style
    """

    # Validate topic
    if not request.topic or len(request.topic.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Topic must be at least 3 characters long"
        )

    # Generate appropriate prompt
    prompt = generate_lesson_prompt(request.topic, request.style)

    # Call Claude API
    claude_response = call_claude_api(prompt)

    # Format response based on style
    if request.style == "text":
        return {
            "type": "text",
            "content": claude_response
        }

    elif request.style == "voice":
        audio_base64, mime_type = synthesize_speech(claude_response)
        return {
            "type": "voice",
            "content": claude_response,
            "audio_base64": audio_base64,
            "mime_type": mime_type
        }

    elif request.style == "visual":
        try:
            # Parse JSON slides from Claude response
            # Clean up the response to extract JSON
            json_str = claude_response.strip()

            # Remove markdown code blocks if present
            if json_str.startswith("```"):
                lines = json_str.split("\n")
                json_str = "\n".join(lines[1:-1])

            slides = json.loads(json_str)

            # Validate slides structure
            if not isinstance(slides, list) or len(slides) != 5:
                raise ValueError("Expected exactly 5 slides")

            # Generate images for each slide
            for slide in slides:
                if "image_prompt" in slide:
                    # Generate image using Hugging Face
                    slide["image"] = generate_image_hf(slide["image_prompt"])

            return {
                "type": "slides",
                "slides": slides
            }
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse visual content: {str(e)}"
            )

    raise HTTPException(status_code=400, detail="Invalid style parameter")


@app.get("/health")
async def health_check():
    """Detailed health check for deployment"""
    anthropic_api_key_set = bool(os.getenv("ANTHROPIC_API_KEY"))
    elevenlabs_api_key_set = bool(ELEVENLABS_API_KEY)
    return {
        "status": "healthy" if anthropic_api_key_set and elevenlabs_api_key_set else "degraded",
        "anthropic_api_key_configured": anthropic_api_key_set,
        "elevenlabs_api_key_configured": elevenlabs_api_key_set,
        "message": (
            "Ready to generate lessons"
            if anthropic_api_key_set and elevenlabs_api_key_set
            else "ANTHROPIC_API_KEY or ELEVENLABS_API_KEY not set"
        )
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
