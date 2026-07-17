from google import genai
from google.genai import types

from app.core.config import settings

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

def call_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )

    return response.text or ""