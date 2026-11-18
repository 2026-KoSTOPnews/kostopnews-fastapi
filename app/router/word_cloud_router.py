from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.cache import cache
from app.core.date import get_today_kst

from app.infrastructure.database import get_db
from app.schema.word_cloud import WordCloudResponse
from app.service.word_cloud_service import get_company_word_cloud

router = APIRouter(prefix="/api/companies", tags=["Word Cloud"],)

@router.get("/{company_id}/word-cloud", response_model=WordCloudResponse)
def read_company_word_cloud(
    company_id: int,
    target_date: date = Query(default_factory=get_today_kst),
    period_type: str = Query("daily", pattern="^(daily|weekly|monthly)$"),
    text_type: str = Query("title", pattern="^(title|content)$"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    cache_key = (
        "word-cloud",
        company_id,
        target_date,
        period_type,
        text_type,
        limit,
    )

    yesterday = get_today_kst() - timedelta(days=1)

    if target_date == yesterday:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    result = get_company_word_cloud(
        db,
        company_id,
        target_date,
        period_type,
        text_type,
        limit,
    )

    if target_date == yesterday:
        cache.set(cache_key, result, ttl=3600)

    return result