from datetime import date
from unittest.mock import patch

from app.core.date import get_today_kst


def test_get_today_kst():
    """KST 기준 오늘 날짜를 반환한다."""
    with patch(
        "app.core.date.datetime"
    ) as mock_datetime:
        mock_datetime.now.return_value.date.return_value = date(2026, 11, 18)

        result = get_today_kst()

    assert result == date(2026, 11, 18)