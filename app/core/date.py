from datetime import date, datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")

def get_today_kst() -> date:
    return datetime.now(KST).date()