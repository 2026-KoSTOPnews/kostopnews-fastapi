from datetime import date, datetime
from types import SimpleNamespace
from unittest.mock import MagicMock

from app.service.news_service import get_news_by_date


def make_article(
    article_id,
    title="테스트 기사",
    pub_date=datetime(2026, 10, 24, 12, 0),
    summary="기사 요약",
    sentiment="positive",
    sentiment_score=0.8,
):
    return SimpleNamespace(
        id=article_id,
        title=title,
        link=f"https://example.com/{article_id}",
        pub_date=pub_date,
        summary=summary,
        sentiment=sentiment,
        sentiment_score=sentiment_score,
    )


def test_get_news_by_date_returns_articles_and_keywords(db):
    """기사 정보와 해당 기사의 키워드를 반환한다."""
    article = make_article(1)

    db.execute.side_effect = [
        MagicMock(all=MagicMock(return_value=[article])),
        MagicMock(
            all=MagicMock(
                return_value=[
                    (1, "AI"),
                    (1, "반도체"),
                ]
            )
        ),
    ]

    result = get_news_by_date(
        db=db,
        company_id=10,
        target_date=date(2026, 10, 24),
        page=1,
        size=5,
    )

    assert result["has_next"] is False
    assert len(result["items"]) == 1
    assert result["items"][0] == {
        "id": 1,
        "title": "테스트 기사",
        "link": "https://example.com/1",
        "pub_date": datetime(2026, 10, 24, 12, 0),
        "summary": "기사 요약",
        "sentiment": "positive",
        "sentiment_score": 0.8,
        "keywords": ["AI", "반도체"],
    }

    # 기사 조회 1회 + 키워드 일괄 조회 1회
    assert db.execute.call_count == 2


def test_get_news_by_date_fetches_keywords_in_one_query(db):
    """여러 기사의 키워드를 하나의 추가 쿼리로 조회한다."""
    articles = [
        make_article(1, title="첫 번째 기사"),
        make_article(2, title="두 번째 기사"),
    ]

    db.execute.side_effect = [
        MagicMock(all=MagicMock(return_value=articles)),
        MagicMock(
            all=MagicMock(
                return_value=[
                    (1, "AI"),
                    (1, "클라우드"),
                    (2, "반도체"),
                ]
            )
        ),
    ]

    result = get_news_by_date(
        db=db,
        company_id=10,
        target_date=date(2026, 10, 24),
        size=5,
    )

    assert result["items"][0]["keywords"] == ["AI", "클라우드"]
    assert result["items"][1]["keywords"] == ["반도체"]
    assert db.execute.call_count == 2


def test_get_news_by_date_returns_empty_result(db):
    """조회된 기사가 없으면 빈 목록을 반환하고 키워드 쿼리를 실행하지 않는다."""
    db.execute.return_value.all.return_value = []

    result = get_news_by_date(
        db=db,
        company_id=10,
        target_date=date(2026, 10, 24),
    )

    assert result == {
        "items": [],
        "has_next": False,
    }
    assert db.execute.call_count == 1


def test_get_news_by_date_detects_next_page(db):
    """size보다 많은 결과가 조회되면 다음 페이지가 있다고 판단한다."""
    articles = [
        make_article(1),
        make_article(2),
        make_article(3),
    ]

    db.execute.side_effect = [
        MagicMock(all=MagicMock(return_value=articles)),
        MagicMock(
            all=MagicMock(
                return_value=[
                    (1, "AI"),
                    (2, "클라우드"),
                ]
            )
        ),
    ]

    result = get_news_by_date(
        db=db,
        company_id=10,
        target_date=date(2026, 10, 24),
        page=1,
        size=2,
    )

    assert result["has_next"] is True
    assert len(result["items"]) == 2
    assert [item["id"] for item in result["items"]] == [1, 2]
    assert db.execute.call_count == 2