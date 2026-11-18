from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.cache import cache
from app.core.date import get_today_kst

from app.infrastructure.database import get_db
from app.schema.keyword import CompanyKeywordResponse
from app.schema.news import NewsPageResponse
from app.schema.sentiment import CompanySentimentResponse
from app.service.keyword_service import get_company_keywords
from app.service.news_service import get_news_by_date
from app.service.sentiment_service import get_company_sentiment

router = APIRouter(prefix="/api/companies", tags=["News"])

@router.get("/{company_id}/sentiment", response_model=CompanySentimentResponse)
def read_company_sentiment(
    company_id: int,
    target_date: date = Query(default_factory=get_today_kst),
    db: Session = Depends(get_db),
):
    cache_key = ("sentiment", company_id, target_date)
    yesterday = get_today_kst() - timedelta(days=1)

    if target_date == yesterday:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    result = get_company_sentiment(db, company_id, target_date)

    if target_date == yesterday:
        cache.set(cache_key, result, ttl=3600)

    return result

@router.get("/{company_id}/keywords", response_model=CompanyKeywordResponse)
def read_company_keywords(
    company_id: int,
    target_date: date = Query(default_factory=get_today_kst),
    db: Session = Depends(get_db),
):
    cache_key = ("keywords", company_id, target_date)
    yesterday = get_today_kst() - timedelta(days=1)

    if target_date == yesterday:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    result = get_company_keywords(db, company_id, target_date)

    if target_date == yesterday:
        cache.set(cache_key, result, ttl=3600)

    return result

@router.get("/{company_id}/news", response_model=NewsPageResponse)
def read_company_news(
    company_id: int,
    target_date: date = Query(default_factory=get_today_kst),
    page: int = Query(1, ge=1),
    size: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    today = get_today_kst()
    yesterday = today - timedelta(days=1)

    cache_key = ("news", company_id, target_date, page, size)
    cache_enabled = target_date in (today, yesterday)

    if cache_enabled:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    result = get_news_by_date(db, company_id, target_date, page, size)

    if cache_enabled:
        cache.set(cache_key, result, ttl=600)

    return result