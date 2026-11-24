from datetime import date
from uuid import uuid4

from sqlalchemy import text

from app.service.news_service import get_news_by_date


def test_get_news_by_date_integration_without_analysis(real_db):
    """PostgreSQL에서 기업 멘션을 기준으로 분석 결과 없는 기사도 조회되는지 검증한다."""
    db = real_db

    suffix = uuid4().hex
    target_date = date(2026, 10, 26)

    # 테스트용 기업 2개 생성
    company_ids = []
    for i in range(2):
        company_id = db.execute(
            text("""
                INSERT INTO companies (name, name_kr)
                VALUES (:name, :name_kr)
                RETURNING id
            """),
            {
                "name": f"test-company-{suffix}-{i}",
                "name_kr": f"테스트 기업 {suffix} {i}",
            },
        ).scalar_one()
        company_ids.append(company_id)

    target_company_id, other_company_id = company_ids

    # 기사 2개 생성: 첫 번째 기사에만 조회 대상 기업의 멘션이 있음
    article_ids = []
    for i in range(2):
        article_id = db.execute(
            text("""
                INSERT INTO news_articles (title, link, pub_date, source, content)
                VALUES (:title, :link, :pub_date, :source, :content)
                RETURNING id
            """),
            {
                "title": f"테스트 뉴스 {suffix} {i}",
                "link": f"https://example.com/{suffix}/{i}",
                "pub_date": target_date,
                "source": "test",
                "content": "테스트 기사 내용",
            },
        ).scalar_one()
        article_ids.append(article_id)

    # 첫 번째 기사는 대상 기업, 두 번째 기사는 다른 기업과 연결
    db.execute(
        text("""
            INSERT INTO news_mentions (article_id, company_id)
            VALUES (:article_id, :company_id)
        """),
        {
            "article_id": article_ids[0],
            "company_id": target_company_id,
        },
    )
    db.execute(
        text("""
            INSERT INTO news_mentions (article_id, company_id)
            VALUES (:article_id, :company_id)
        """),
        {
            "article_id": article_ids[1],
            "company_id": other_company_id,
        },
    )

    # 감성 분석 및 키워드 데이터는 의도적으로 생성하지 않음
    db.flush()

    result = get_news_by_date(
        db=db,
        company_id=target_company_id,
        target_date=target_date,
        page=1,
        size=5,
    )

    assert len(result["items"]) == 1
    assert result["has_next"] is False

    article = result["items"][0]
    assert article["id"] == article_ids[0]
    assert article["title"] == f"테스트 뉴스 {suffix} 0"
    assert article["summary"] is None
    assert article["sentiment"] is None
    assert article["sentiment_score"] is None
    assert article["keywords"] == []