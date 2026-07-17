import json
import time
import logging

from app.infrastructure.llm.llm_client import call_llm
from app.infrastructure.llm.prompts import sentiment_prompt
from app.schema.sentiment import SentimentResponse, SentimentRequest

logger = logging.getLogger(__name__)

MAX_RETRY = 3
RETRY_DELAY = 30

def analyze_sentiment_batch_service(reqs: list[SentimentRequest]) -> list[SentimentResponse]:
    results = []

    for req in reqs:
        result = analyze_sentiment_service(req)

        if result is not None:
            results.append(result)

        time.sleep(10)

    return results

def analyze_sentiment_service(req) -> SentimentResponse | None:
    prompt = sentiment_prompt(
        req.company_name,
        req.title,
        req.content
    )

    for attempt in range(MAX_RETRY):
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
                MAX_RETRY,
                e,
            )

            if attempt < MAX_RETRY - 1:
                time.sleep(RETRY_DELAY)

    return None