from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

from app.core.config import settings
from app.infrastructure.llm.llm_client import call_llm, create_llm_client


@pytest.mark.asyncio
async def test_call_llm_uses_solar_pro4(monkeypatch):
    """LLM 모델로 Solar Pro 4를 사용하는지 확인한다."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content='{"sentiment": "positive"}'))
    ]

    mock_client.chat.completions.create = AsyncMock(
        return_value=mock_response
    )

    monkeypatch.setattr(settings, "SOLAR_MODEL", "solar-pro4")

    result = await call_llm(mock_client, "테스트 프롬프트")

    mock_client.chat.completions.create.assert_awaited_once_with(
        model="solar-pro4",
        messages=[
            {
                "role": "user",
                "content": "테스트 프롬프트",
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    assert result == '{"sentiment": "positive"}'


def test_create_llm_client():
    """Upstage AsyncOpenAI 클라이언트를 올바르게 생성한다."""
    with patch(
        "app.infrastructure.llm.llm_client.AsyncOpenAI"
    ) as mock_async_openai:
        client = create_llm_client()

    mock_async_openai.assert_called_once_with(
        api_key=settings.UPSTAGE_API_KEY,
        base_url="https://api.upstage.ai/v1",
    )
    assert client is mock_async_openai.return_value


@pytest.mark.asyncio
async def test_call_llm_returns_response_content():
    """LLM 응답의 content를 문자열로 반환한다."""
    client = MagicMock()
    client.chat.completions.create = AsyncMock(
        return_value=SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content='{"summary": "테스트 요약"}'
                    )
                )
            ]
        )
    )

    result = await call_llm(client, "테스트 프롬프트")

    assert result == '{"summary": "테스트 요약"}'
    client.chat.completions.create.assert_awaited_once_with(
        model=settings.SOLAR_MODEL,
        messages=[
            {
                "role": "user",
                "content": "테스트 프롬프트",
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )


@pytest.mark.asyncio
async def test_call_llm_returns_empty_string_when_content_is_none():
    """LLM 응답 content가 None이면 빈 문자열을 반환한다."""
    client = MagicMock()
    client.chat.completions.create = AsyncMock(
        return_value=SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=None)
                )
            ]
        )
    )

    result = await call_llm(client, "테스트 프롬프트")

    assert result == ""