from datetime import date
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.router import (
    company_router,
    news_router,
    analysis_router,
    word_cloud_router,
)
from app.infrastructure.database import get_db
from app.schema.word_cloud import WordCloudResponse


def override_get_db():
    yield None


app = FastAPI()

app.include_router(company_router.router)
app.include_router(news_router.router)
app.include_router(analysis_router.router)
app.include_router(word_cloud_router.router)

app.dependency_overrides[get_db] = override_get_db


def test_word_cloud_uses_today_when_target_date_is_omitted():
    """날짜 미입력 시 KST 기준 오늘 날짜를 사용한다."""

    with patch(
        "app.router.word_cloud_router.get_company_word_cloud"
    ) as mock_service:
        mock_service.return_value = WordCloudResponse(
            company_id=1,
            period_type="daily",
            period_start=date.today(),
            period_end=date.today(),
            text_type="title",
            words=[],
        )

        with TestClient(app) as client:
            response = client.get("/api/companies/1/word-cloud")

    assert response.status_code == 200
    assert response.json()["period_start"] == date.today().isoformat()
    assert mock_service.call_args.args[2] == date.today()