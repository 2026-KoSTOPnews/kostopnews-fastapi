from fastapi import Request

import asyncio
import json
import logging
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.infrastructure.llm.llm_client import call_llm, llm_semaphore
from app.infrastructure.llm.prompts import sentiment_prompt
from app.infrastructure.models.news_sentiment_aggregate import NewsSentimentAggregate
from app.schema.sentiment import SentimentResponse, SentimentRequest

logger = logging.getLogger(__name__)

def get_company_sentiment(db: Session, company_id: int, target_date: date) -> dict:
    def get_aggregates(period_type: str, limit: int):
        result = db.execute(
            select(NewsSentimentAggregate)
            .where(
                NewsSentimentAggregate.company_id == company_id,
                NewsSentimentAggregate.period_type == period_type,
                NewsSentimentAggregate.period_start <= target_date,
            )
            .order_by(
                NewsSentimentAggregate.period_start.desc()
            )
            .limit(limit)
        )

        rows = list(result.scalars().all())

        return list(reversed(rows))

    return {
        "daily": get_aggregates("DAILY", 30),
        "weekly": get_aggregates("WEEKLY", 12),
        "monthly": get_aggregates("MONTHLY", 12),
    }

async def analyze_sentiment_batch_service(reqs: list[SentimentRequest], request: Request) -> list[SentimentResponse]:
    async def analyze_with_limit(req: SentimentRequest) -> SentimentResponse | None:
        async with llm_semaphore:
            return await analyze_sentiment_service(req, request)

    results = await asyncio.gather(*(analyze_with_limit(req) for req in reqs))

    return [result for result in results if result is not None]

async def analyze_sentiment_service(req: SentimentRequest, request: Request) -> SentimentResponse | None:
    client = request.app.state.llm_client
    prompt = sentiment_prompt(req.company_name, req.title, req.content)

    for attempt in range(settings.MAX_RETRY):
        try:
            result = await call_llm(client, prompt)
            parsed = json.loads(result)

            return SentimentResponse(
                article_id=req.article_id,
                company_id=req.company_id,
                summary=parsed["summary"],
                sentiment=parsed["sentiment"],
                score=parsed["score"],
                reason=parsed["reason"],
            )

        except Exception as e:
            logger.warning(
                "Sentiment analysis failed | article_id=%s | retry=%d/%d | error=%s",
                req.article_id,
                attempt + 1,
                settings.MAX_RETRY,
                e,
            )

            if attempt < settings.MAX_RETRY - 1:
                await asyncio.sleep(settings.RETRY_DELAY * (2 ** attempt))

    return None