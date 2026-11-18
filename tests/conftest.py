from types import SimpleNamespace
from unittest.mock import MagicMock

import os

import pytest

from sqlalchemy import create_engine
from app.infrastructure.database import Base, create_db_engine, create_session_factory
from app.infrastructure.models.company import Company

from dotenv import load_dotenv


load_dotenv(".env.test")


@pytest.fixture
def test_engine():
    database_url = os.getenv("TEST_DATABASE_URL")

    if not database_url:
        pytest.fail("TEST_DATABASE_URL 환경변수가 설정되지 않았습니다.")

    engine = create_engine(database_url)

    Base.metadata.drop_all(
        bind=engine,
        tables=[Company.__table__],
    )

    Base.metadata.create_all(
        bind=engine,
        tables=[Company.__table__],
    )

    yield engine

    Base.metadata.drop_all(
        bind=engine,
        tables=[Company.__table__],
    )

    engine.dispose()


@pytest.fixture
def real_db():
    engine = create_db_engine()
    TestingSessionLocal = create_session_factory(engine)

    with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            session.rollback()

    engine.dispose()


@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def mock_request():
    req = MagicMock()
    req.app.state.llm_client = MagicMock()
    return req


@pytest.fixture
def sentiment_request():
    return SimpleNamespace(
        article_id=1,
        company_id=10,
        company_name="테스트 기업",
        title="테스트 기사",
        content="테스트 기사 내용",
    )


@pytest.fixture
def keyword_request():
    return SimpleNamespace(
        article_id=1,
        title="테스트 기사",
        content="테스트 기사 내용",
    )