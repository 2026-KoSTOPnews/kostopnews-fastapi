from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.infrastructure.models.news_word_aggregate import NewsWordAggregate
from app.schema.word_cloud import WordCloudItem, WordCloudResponse

def get_period_range(target_date: date, period_type: str) -> tuple[date, date]:
    if period_type == "daily":
        start_date = target_date
        end_date = start_date + timedelta(days=1)
    elif period_type == "weekly":
        start_date = target_date - timedelta(days=target_date.weekday())
        end_date = start_date + timedelta(days=7)
    elif period_type == "monthly":
        start_date = target_date.replace(day=1)
        end_date = start_date + relativedelta(months=1)
    else:
        raise ValueError("Unsupported period_type")

    return start_date, end_date

def get_company_word_cloud(db: Session, company_id: int, target_date: date, period_type: str, text_type: str, limit: int) -> WordCloudResponse:
    start_date, end_date = get_period_range(
        target_date,
        period_type,
    )

    query = (
        select(
            NewsWordAggregate.word,
            func.sum(NewsWordAggregate.count).label("count"),
        )
        .where(
            NewsWordAggregate.company_id == company_id,
            NewsWordAggregate.text_type == text_type,
            NewsWordAggregate.period_start >= start_date,
            NewsWordAggregate.period_start < end_date,
        )
        .group_by(NewsWordAggregate.word)
        .order_by(func.sum(NewsWordAggregate.count).desc())
        .limit(limit)
    )

    rows = db.execute(query).all()

    return WordCloudResponse(
        company_id=company_id,
        period_type=period_type,
        period_start=start_date,
        period_end=end_date - timedelta(days=1),
        text_type=text_type,
        words=[
            WordCloudItem(
                word=row.word,
                count=row.count,
            )
            for row in rows
        ],
    )