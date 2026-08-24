import json
import time
import logging
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.infrastructure.llm.llm_client import call_llm
from app.infrastructure.llm.prompts import sentiment_prompt
from app.infrastructure.models.news_sentiment_aggregate import NewsSentimentAggregate
from app.schema.sentiment import SentimentResponse, SentimentRequest

logger = logging.getLogger(__name__)

def get_company_sentiment(db: Session, company_id: int, target_date: date) -> dict:
    daily_end = target_date

    weekly_end = target_date - timedelta(days=target_date.weekday())

    monthly_end = target_date.replace(day=1)

    def get_aggregates(period_type: str, end_date: date, limit: int):
        result = db.execute(
            select(NewsSentimentAggregate)
            .where(
                NewsSentimentAggregate.company_id == company_id,
                NewsSentimentAggregate.period_type == period_type,
                NewsSentimentAggregate.period_start <= end_date,
            )
            .order_by(
                NewsSentimentAggregate.period_start.desc()
            )
            .limit(limit)
        )

        return list(reversed(result.scalars().all()))

    return {
        "daily": get_aggregates(
            "DAILY",
            daily_end,
            30,
        ),
        "weekly": get_aggregates(
            "WEEKLY",
            weekly_end,
            12,
        ),
        "monthly": get_aggregates(
            "MONTHLY",
            monthly_end,
            12,
        ),
    }

def analyze_sentiment_batch_service(reqs: list[SentimentRequest]) -> list[SentimentResponse]:
    results = []

    for req in reqs:
        result = analyze_sentiment_service(req)

        if result is not None:
            results.append(result)

        time.sleep(1)

    return results

def analyze_sentiment_service(req) -> SentimentResponse | None:
    prompt = sentiment_prompt(
        req.company_name,
        req.title,
        req.content
    )

    for attempt in range(settings.MAX_RETRY):
        try:
            result = call_llm(prompt)

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
                time.sleep(settings.RETRY_DELAY)

    return None