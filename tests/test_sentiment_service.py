import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.core.config import settings
from app.service.sentiment_service import analyze_sentiment_service, analyze_sentiment_batch_service


@pytest.mark.asyncio
async def test_analyze_sentiment_service_success(mock_request, sentiment_request):
    """감성 분석 결과를 정상적으로 반환한다."""
    response = (
        '{"summary": "기업 실적 개선", '
        '"sentiment": "positive", '
        '"score": 0.8, '
        '"reason": "실적 개선 소식"}'
    )

    with patch(
        "app.service.sentiment_service.call_llm",
        new_callable=AsyncMock,
        return_value=response,
    ) as mock_call:
        result = await analyze_sentiment_service(sentiment_request, mock_request)

    assert result.article_id == 1
    assert result.company_id == 10
    assert result.summary == "기업 실적 개선"
    assert result.sentiment == "positive"
    assert result.score == 0.8
    assert result.reason == "실적 개선 소식"
    mock_call.assert_awaited_once()


@pytest.mark.asyncio
async def test_analyze_sentiment_service_retries_on_failure(mock_request, sentiment_request, monkeypatch):
    """감성 분석 실패 시 재시도한다."""
    monkeypatch.setattr(settings, "MAX_RETRY", 3)

    response = (
        '{"summary": "요약", "sentiment": "neutral", '
        '"score": 0.0, "reason": "중립"}'
    )

    with (
        patch(
            "app.service.sentiment_service.call_llm",
            new_callable=AsyncMock,
            side_effect=[Exception("API error"), response],
        ) as mock_call,
        patch(
            "app.service.sentiment_service.asyncio.sleep",
            new_callable=AsyncMock,
        ) as mock_sleep,
    ):
        result = await analyze_sentiment_service(sentiment_request, mock_request)

    assert result.sentiment == "neutral"
    assert mock_call.await_count == 2
    mock_sleep.assert_awaited_once()


@pytest.mark.asyncio
async def test_analyze_sentiment_service_returns_none_after_retries(mock_request, sentiment_request, monkeypatch):
    """최대 재시도 횟수를 초과하면 None을 반환한다."""
    monkeypatch.setattr(settings, "MAX_RETRY", 3)

    with (
        patch(
            "app.service.sentiment_service.call_llm",
            new_callable=AsyncMock,
            side_effect=Exception("API error"),
        ) as mock_call,
        patch(
            "app.service.sentiment_service.asyncio.sleep",
            new_callable=AsyncMock,
        ),
    ):
        result = await analyze_sentiment_service(sentiment_request, mock_request)

    assert result is None
    assert mock_call.await_count == 3


@pytest.mark.asyncio
async def test_analyze_sentiment_service_retries_on_invalid_json(mock_request, sentiment_request, monkeypatch):
    """잘못된 JSON 응답이면 재시도한다."""
    monkeypatch.setattr(settings, "MAX_RETRY", 3)

    response = (
        '{"summary": "요약", "sentiment": "positive", '
        '"score": 0.7, "reason": "긍정"}'
    )

    with (
        patch(
            "app.service.sentiment_service.call_llm",
            new_callable=AsyncMock,
            side_effect=["invalid json", response],
        ) as mock_call,
        patch(
            "app.service.sentiment_service.asyncio.sleep",
            new_callable=AsyncMock,
        ),
    ):
        result = await analyze_sentiment_service(sentiment_request, mock_request)

    assert result.sentiment == "positive"
    assert mock_call.await_count == 2


@pytest.mark.asyncio
async def test_analyze_sentiment_batch_service_filters_failed_results(mock_request, sentiment_request):
    """배치 처리 결과에서 실패한 항목을 제외한다."""
    second_request = SimpleNamespace(
        article_id=2,
        company_id=20,
        company_name="다른 기업",
        title="두 번째 기사",
        content="두 번째 기사 내용",
    )

    with patch(
        "app.service.sentiment_service.analyze_sentiment_service",
        new_callable=AsyncMock,
        side_effect=[
            SimpleNamespace(article_id=1, company_id=10),
            None,
        ],
    ):
        results = await analyze_sentiment_batch_service([sentiment_request, second_request], mock_request)

    assert len(results) == 1
    assert results[0].article_id == 1


@pytest.mark.asyncio
async def test_analyze_sentiment_batch_service_limits_concurrency(mock_request, monkeypatch):
    """배치 처리 시 공유 세마포어로 동시 실행 개수를 제한한다."""
    import app.infrastructure.llm.llm_client as llm_client
    import app.service.sentiment_service as service

    semaphore = asyncio.Semaphore(2)

    monkeypatch.setattr(llm_client, "llm_semaphore", semaphore)
    monkeypatch.setattr(service, "llm_semaphore", semaphore)

    reqs = [
        SimpleNamespace(
            article_id=i,
            company_id=i,
            company_name=f"기업 {i}",
            title=f"기사 {i}",
            content="내용",
        )
        for i in range(5)
    ]

    active = 0
    max_active = 0

    async def mock_analyze(req, _request):
        nonlocal active, max_active

        active += 1
        max_active = max(max_active, active)

        try:
            await asyncio.sleep(0.01)
            return SimpleNamespace(
                article_id=req.article_id,
                company_id=req.company_id,
            )
        finally:
            active -= 1

    with patch(
        "app.service.sentiment_service.analyze_sentiment_service",
        side_effect=mock_analyze,
    ):
        results = await service.analyze_sentiment_batch_service(
            reqs, mock_request
        )

    assert len(results) == 5
    assert max_active == 2