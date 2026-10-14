from openai import OpenAI

from app.core.config import settings

_client: OpenAI | None = None

def create_llm_client() -> OpenAI:
    return OpenAI(
        api_key=settings.UPSTAGE_API_KEY,
        base_url="https://api.upstage.ai/v1",
    )

def call_llm(client: OpenAI, prompt: str) -> str:
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