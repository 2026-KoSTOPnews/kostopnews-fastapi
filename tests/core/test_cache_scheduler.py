from datetime import datetime
from unittest.mock import patch

from zoneinfo import ZoneInfo

from app.core.cache_scheduler import get_next_cache_schedule

KST = ZoneInfo("Asia/Seoul")


def test_news_cache_schedule():
    """뉴스 캐시는 매시 15분, 25분, 35분에 초기화한다."""
    fixed_now = datetime(2026, 11, 18, 17, 10, tzinfo=KST)

    with patch("app.core.cache_scheduler.datetime", wraps=datetime) as mock_datetime:
        mock_datetime.now.return_value = fixed_now

        next_run, prefix = get_next_cache_schedule()

    assert next_run == datetime(2026, 11, 18, 17, 15, tzinfo=KST)
    assert prefix == "news"


def test_word_cloud_cache_schedule():
    """워드 클라우드 캐시는 매일 01:50에 초기화한다."""
    fixed_now = datetime(2026, 11, 18, 1, 35, tzinfo=KST)

    with patch("app.core.cache_scheduler.datetime", wraps=datetime) as mock_datetime:
        mock_datetime.now.return_value = fixed_now

        next_run, prefix = get_next_cache_schedule()

    assert next_run == datetime(2026, 11, 18, 1, 50, tzinfo=KST)
    assert prefix == "word-cloud"


def test_sentiment_cache_schedule():
    """감성 분석 캐시는 매일 03:50에 초기화한다."""
    fixed_now = datetime(2026, 11, 18, 3, 35, tzinfo=KST)

    with patch("app.core.cache_scheduler.datetime", wraps=datetime) as mock_datetime:
        mock_datetime.now.return_value = fixed_now

        next_run, prefix = get_next_cache_schedule()

    assert next_run == datetime(2026, 11, 18, 3, 50, tzinfo=KST)
    assert prefix == "sentiment"


def test_keyword_cache_schedule():
    """키워드 캐시는 매일 04:50에 초기화한다."""
    fixed_now = datetime(2026, 11, 18, 4, 35, tzinfo=KST)

    with patch("app.core.cache_scheduler.datetime", wraps=datetime) as mock_datetime:
        mock_datetime.now.return_value = fixed_now

        next_run, prefix = get_next_cache_schedule()

    assert next_run == datetime(2026, 11, 18, 4, 50, tzinfo=KST)
    assert prefix == "keywords"


def test_schedule_moves_to_next_day():
    """오늘의 초기화 일정이 모두 지났으면 다음 날 일정을 반환한다."""
    fixed_now = datetime(2026, 11, 18, 23, 56, tzinfo=KST)

    with patch("app.core.cache_scheduler.datetime", wraps=datetime) as mock_datetime:
        mock_datetime.now.return_value = fixed_now

        next_run, prefix = get_next_cache_schedule()

    assert next_run == datetime(2026, 11, 19, 0, 15, tzinfo=KST)
    assert prefix == "news"