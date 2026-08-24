# from google import genai
# from google.genai import types
from openai import OpenAI

from app.core.config import settings

client = OpenAI(
    api_key=settings.UPSTAGE_API_KEY,
    base_url="https://api.upstage.ai/v1",
)

def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=settings.SOLAR_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content or ""

# client = genai.Client(api_key=settings.GEMINI_API_KEY)
#
# def call_llm(prompt: str) -> str:
#     response = client.models.generate_content(
#         model=settings.GEMINI_MODEL,
#         contents=prompt,
#         config=types.GenerateContentConfig(
#             response_mime_type="application/json",
#             temperature=0.2,
#         ),
#     )
#
#     return response.text or ""