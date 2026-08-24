import json
import time
import logging

from app.core.config import settings
from app.infrastructure.llm.llm_client import call_llm
from app.infrastructure.llm.prompts import keyword_prompt
from app.schema.keyword import KeywordsRequest, KeywordsResponse

logger = logging.getLogger(__name__)

def extract_keywords_batch_service(reqs: list[KeywordsRequest]) -> list[KeywordsResponse]:
    results = []

    for req in reqs:
        result = extract_keywords_service(req)

        if result is not None:
            results.append(result)

        time.sleep(1)

    return results

def extract_keywords_service(req: KeywordsRequest,) -> KeywordsResponse | None:
    prompt = keyword_prompt(req.title, req.content,)

    for attempt in range(settings.MAX_RETRY):
        try:
            result = call_llm(prompt)

            parsed = json.loads(result)

            return KeywordsResponse(
                article_id=req.article_id,
                keywords=parsed["keywords"],
            )

        except Exception as e:
            logger.warning(
                "Keyword extraction failed | article_id=%s | retry=%d/%d | error=%s",
                req.article_id,
                attempt + 1,
                settings.MAX_RETRY,
                e,
            )

            if attempt < settings.MAX_RETRY - 1:
                time.sleep(settings.RETRY_DELAY)

    logger.error(
        "Keyword extraction failed after retries | article_id=%s",
        req.article_id,
    )

    return None