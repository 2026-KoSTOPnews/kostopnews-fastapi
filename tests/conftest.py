from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest


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