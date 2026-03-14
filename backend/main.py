"""
MicroLesson AI - FastAPI Backend
Generates personalized 5-minute lessons using Claude API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
import os
from typing import Literal
import json

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

Format as EXACTLY 5 SLIDES in JSON format:
[
  {{"title": "Introduction: [Topic]", "text": "Hook + overview (2-3 sentences)"}},
  {{"title": "Key Concept 1: [Name]", "text": "Explanation (2-3 sentences)"}},
  {{"title": "Key Concept 2: [Name]", "text": "Explanation (2-3 sentences)"}},
  {{"title": "Key Concept 3: [Name]", "text": "Explanation (2-3 sentences)"}},
  {{"title": "Summary & Takeaway", "text": "Recap + key message (2-3 sentences)"}}
]

Return ONLY valid JSON array, no other text."""

    return base_requirements


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
        # For voice, return text that frontend will convert to speech
        return {
            "type": "voice",
            "content": claude_response
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
    api_key_set = bool(os.getenv("ANTHROPIC_API_KEY"))
    return {
        "status": "healthy" if api_key_set else "degraded",
        "api_key_configured": api_key_set,
        "message": "Ready to generate lessons" if api_key_set else "ANTHROPIC_API_KEY not set"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
