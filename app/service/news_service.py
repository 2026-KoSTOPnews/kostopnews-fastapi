from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.models.news_analysis import NewsAnalysis
from app.infrastructure.models.news_article import NewsArticle
from app.infrastructure.models.news_keywords import NewsKeyword

def get_news_by_date(db: Session, company_id: int, target_date: date, page: int = 1, size: int = 5) -> dict:
    start_datetime = datetime.combine(target_date, datetime.min.time())
    end_datetime = start_datetime + timedelta(days=1)

    result = db.execute(
        select(
            NewsArticle.id,
            NewsArticle.title,
            NewsArticle.content,
            NewsArticle.pub_date,
            NewsAnalysis.summary,
            NewsAnalysis.sentiment,
            NewsAnalysis.sentiment_score,
        )
        .join(
            NewsAnalysis,
            NewsAnalysis.article_id == NewsArticle.id,
        )
        .where(
            NewsAnalysis.company_id == company_id,
            NewsArticle.pub_date >= start_datetime,
            NewsArticle.pub_date < end_datetime,
        )
        .order_by(
            NewsArticle.pub_date.desc()
        )
        .offset((page - 1) * size)
        .limit(size + 1)
    )

    articles = result.all()

    has_next = len(articles) == size + 1

    articles = articles[:size]

    response = []

    for article in articles:
        keyword_result = db.execute(
            select(NewsKeyword.keyword)
            .where(
                NewsKeyword.article_id == article.id
            )
            .order_by(NewsKeyword.id)
        )

        keywords = list(
            keyword_result.scalars().all()
        )

        response.append(
            {
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "pub_date": article.pub_date,
                "summary": article.summary,
                "sentiment": article.sentiment,
                "sentiment_score": article.sentiment_score,
                "keywords": keywords,
            }
        )

    return {
        "items": response,
        "has_next": has_next,
    }