from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.models.news_analysis import NewsAnalysis
from app.infrastructure.models.news_article import NewsArticle
from app.infrastructure.models.news_keywords import NewsKeyword
from app.infrastructure.models.news_mention import NewsMention

def get_news_by_date(db: Session, company_id: int, target_date: date, page: int = 1, size: int = 5) -> dict:
    start_datetime = datetime.combine(target_date, datetime.min.time())
    end_datetime = start_datetime + timedelta(days=1)

    result = db.execute(
        select(
            NewsArticle.id,
            NewsArticle.title,
            NewsArticle.link,
            NewsArticle.pub_date,
            NewsAnalysis.summary,
            NewsAnalysis.sentiment,
            NewsAnalysis.sentiment_score,
        )
        .outerjoin(
            NewsAnalysis,
            (NewsAnalysis.article_id == NewsArticle.id)
            & (NewsAnalysis.company_id == company_id),
        )
        .where(
            NewsArticle.pub_date >= start_datetime,
            NewsArticle.pub_date < end_datetime,
            select(NewsMention.article_id)
            .where(
                NewsMention.article_id == NewsArticle.id,
                NewsMention.company_id == company_id,
            )
            .exists(),
        )
        .order_by(NewsArticle.pub_date.desc())
        .offset((page - 1) * size)
        .limit(size + 1)
    )

    articles = result.all()
    has_next = len(articles) > size
    articles = articles[:size]

    article_ids = [article.id for article in articles]
    keywords_by_article = {article_id: [] for article_id in article_ids}

    if article_ids:
        keyword_result = db.execute(
            select(
                NewsKeyword.article_id,
                NewsKeyword.keyword,
            )
            .where(NewsKeyword.article_id.in_(article_ids))
            .order_by(NewsKeyword.article_id, NewsKeyword.id)
        )

        for article_id, keyword in keyword_result.all():
            keywords_by_article[article_id].append(keyword)

    response = [
        {
            "id": article.id,
            "title": article.title,
            "link": article.link,
            "pub_date": article.pub_date,
            "summary": article.summary,
            "sentiment": article.sentiment,
            "sentiment_score": article.sentiment_score,
            "keywords": keywords_by_article[article.id],
        }
        for article in articles
    ]

    return {
        "items": response,
        "has_next": has_next,
    }