from sqlalchemy import text

from app.infrastructure.database import Base
from app.infrastructure.database_init import initialize_companies
from app.infrastructure.models.company import Company
import app.infrastructure.models


def test_all_models_registered():
    """모든 모델이 SQLAlchemy metadata에 등록되는지 확인한다."""

    expected_tables = {
        "companies",
        "news_articles",
        "news_mentions",
        "news_analysis",
        "news_keywords",
        "news_keyword_aggregate",
        "news_sentiment_aggregate",
        "news_word_aggregate",
    }

    registered_tables = set(Base.metadata.tables.keys())

    assert expected_tables.issubset(registered_tables)


def test_initialize_companies(test_engine):
    """기업 초기 데이터 10개가 등록되는지 확인한다."""

    initialize_companies(test_engine)

    with test_engine.connect() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM companies")
        ).scalar_one()

    assert count == 10


def test_initialize_companies_no_duplicates(test_engine):
    """초기화 함수를 여러 번 실행해도 중복 등록되지 않는지 확인한다."""

    initialize_companies(test_engine)
    initialize_companies(test_engine)

    with test_engine.connect() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM companies")
        ).scalar_one()

    assert count == 10


def test_initialize_companies_preserves_existing_data(test_engine):
    """이미 존재하는 기업의 정보가 변경되지 않는지 확인한다."""

    with test_engine.begin() as connection:
        connection.execute(
            text("""
                INSERT INTO companies (
                    name, name_kr, ticker, sector, aliases
                )
                VALUES (
                    :name, :name_kr, :ticker, :sector, :aliases
                )
            """),
            {
                "name": "삼성전자",
                "name_kr": "기존 기업명",
                "ticker": "TEST001",
                "sector": "기존 업종",
                "aliases": ["기존 별칭"],
            },
        )

    initialize_companies(test_engine)

    with test_engine.connect() as connection:
        company = connection.execute(
            text("""
                SELECT name_kr, ticker, sector, aliases
                FROM companies
                WHERE name = '삼성전자'
            """)
        ).mappings().one()

        count = connection.execute(
            text("SELECT COUNT(*) FROM companies")
        ).scalar_one()

    assert count == 10
    assert company["name_kr"] == "기존 기업명"
    assert company["ticker"] == "TEST001"
    assert company["sector"] == "기존 업종"
    assert company["aliases"] == ["기존 별칭"]