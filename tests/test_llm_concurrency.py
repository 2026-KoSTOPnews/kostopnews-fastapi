import asyncio
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest


@pytest.mark.asyncio
async def test_keyword_and_sentiment_batches_share_concurrency_limit(mock_request, monkeypatch):
    """키워드·감성 분석 배치 전체의 동시 실행 수를 제한한다."""
    import app.infrastructure.llm.llm_client as llm_client
    import app.service.keyword_service as keyword_service
    import app.service.sentiment_service as sentiment_service

    semaphore = asyncio.Semaphore(2)

    # 두 서비스가 동일한 세마포어를 사용하도록 설정
    monkeypatch.setattr(llm_client, "llm_semaphore", semaphore)
    monkeypatch.setattr(keyword_service, "llm_semaphore", semaphore)
    monkeypatch.setattr(sentiment_service, "llm_semaphore", semaphore)

    keyword_reqs = [
        SimpleNamespace(
            article_id=i,
            title=f"기사 {i}",
            content="키워드 분석 테스트",
        )
        for i in range(1, 4)
    ]

    sentiment_reqs = [
        SimpleNamespace(
            article_id=i,
            company_id=i,
            company_name=f"기업 {i}",
            title=f"기사 {i}",
            content="감성 분석 테스트",
        )
        for i in range(4, 7)
    ]

    active = 0
    max_active = 0

    async def mock_keyword(req, _request):
        nonlocal active, max_active
        active += 1
        max_active = max(max_active, active)

        try:
            await asyncio.sleep(0.02)
            return SimpleNamespace(
                article_id=req.article_id,
                keywords=["테스트"],
            )
        finally:
            active -= 1

    async def mock_sentiment(req, _request):
        nonlocal active, max_active
        active += 1
        max_active = max(max_active, active)

        try:
            await asyncio.sleep(0.02)
            return SimpleNamespace(
                article_id=req.article_id,
                company_id=req.company_id,
            )
        finally:
            active -= 1

    with (
        patch(
            "app.service.keyword_service.extract_keywords_service",
            side_effect=mock_keyword,
        ),
        patch(
            "app.service.sentiment_service.analyze_sentiment_service",
            side_effect=mock_sentiment,
        ),
    ):
        keyword_results, sentiment_results = await asyncio.gather(
            keyword_service.extract_keywords_batch_service(
                keyword_reqs, mock_request
            ),
            sentiment_service.analyze_sentiment_batch_service(
                sentiment_reqs, mock_request
            ),
        )

    assert len(keyword_results) == 3
    assert len(sentiment_results) == 3
    assert max_active == 2