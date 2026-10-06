from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

import json
import time
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.infrastructure.llm.llm_client import call_llm
from app.infrastructure.llm.prompts import keyword_prompt
from app.infrastructure.models.news_keyword_aggregate import NewsKeywordAggregate
from app.schema.keyword import KeywordsRequest, KeywordsResponse

logger = logging.getLogger(__name__)

def get_company_keywords(db: Session, company_id: int, target_date: date) -> dict:
    def get_aggregates(period_type: str, keyword_limit: int):

        # 현재 기간 계산
        if period_type == "DAILY":
            period_start = target_date

        elif period_type == "WEEKLY":
            period_start = target_date - timedelta(
                days=target_date.weekday()
            )

        elif period_type == "MONTHLY":
            period_start = target_date.replace(day=1)

        else:
            return {
                "period_start": None,
                "previous_period_start": None,
                "keywords": [],
            }

        # 이전 기간 계산
        if period_type == "DAILY":
            previous_period_start = period_start - timedelta(days=1)

        elif period_type == "WEEKLY":
            previous_period_start = period_start - timedelta(weeks=1)

        elif period_type == "MONTHLY":
            previous_period_start = period_start - relativedelta(months=1)

        # 현재 기간 조회
        current_result = db.execute(
            select(NewsKeywordAggregate)
            .where(
                NewsKeywordAggregate.company_id == company_id,
                NewsKeywordAggregate.period_type == period_type,
                NewsKeywordAggregate.period_start == period_start,
            )
            .order_by(
                NewsKeywordAggregate.count.desc(),
            )
        )

        current_rows = list(current_result.scalars().all())

        if not current_rows:
            return {
                "period_start": None,
                "previous_period_start": previous_period_start,
                "keywords": [],
            }

        # 이전 기간 조회
        previous_result = db.execute(
            select(NewsKeywordAggregate)
            .where(
                NewsKeywordAggregate.company_id == company_id,
                NewsKeywordAggregate.period_type == period_type,
                NewsKeywordAggregate.period_start == previous_period_start,
            )
        )

        previous_rows = list(previous_result.scalars().all())

        previous_counts = {
            row.keyword: row.count
            for row in previous_rows
        }

        # 현재 기간 Top N
        current_rows = current_rows[:keyword_limit]

        keywords = []

        for row in current_rows:
            current_count = row.count
            previous_count = previous_counts.get(row.keyword, 0)

            keywords.append({
                "keyword": row.keyword,
                "count": current_count,
                "previous_count": previous_count,
                "change": current_count - previous_count,
            })

        return {
            "period_start": period_start,
            "previous_period_start": previous_period_start,
            "keywords": keywords,
        }

    return {
        "daily": get_aggregates("DAILY", 5),
        "weekly": get_aggregates("WEEKLY", 5),
        "monthly": get_aggregates("MONTHLY", 5),
    }

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