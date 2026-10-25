from openai import AsyncOpenAI

import asyncio

from app.core.config import settings

MAX_CONCURRENT_REQUESTS = 10

llm_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

_client: AsyncOpenAI | None = None

def create_llm_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=settings.UPSTAGE_API_KEY,
        base_url="https://api.upstage.ai/v1",
    )

async def call_llm(client: AsyncOpenAI, prompt: str) -> str:
    response = await client.chat.completions.create(
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