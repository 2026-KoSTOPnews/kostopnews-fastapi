import json
import pytest

from app.core.config import settings
from app.infrastructure.llm.llm_client import call_llm, create_llm_client


@pytest.mark.integration
@pytest.mark.asyncio
async def test_call_llm_with_real_solar_pro4():
    if not settings.UPSTAGE_API_KEY:
        pytest.skip("UPSTAGE_API_KEY가 설정되지 않았습니다.")

    client = create_llm_client()

    prompt = """
    다음 JSON 형식으로만 응답하라.
    {
      "summary": "기사 핵심 사실을 2~3문장으로 요약",
      "sentiment": "positive | neutral | negative",
      "score": 0.00,
      "reason": "감성 판단 핵심 이유"
    }
    """

    try:
        result = await call_llm(client, prompt)

        assert result.strip()

        parsed = json.loads(result)

        assert "summary" in parsed
        assert "sentiment" in parsed
        assert "score" in parsed
        assert "reason" in parsed

        print(f"\n실제 Solar Pro 4 응답:\n{result}")
    finally:
        await client.close()