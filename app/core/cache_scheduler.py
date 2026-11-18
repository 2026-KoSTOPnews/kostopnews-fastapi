import asyncio
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.core.cache import cache

logger = logging.getLogger(__name__)

KST = ZoneInfo("Asia/Seoul")

def get_next_cache_schedule():
    now = datetime.now(KST)
    schedules = []

    # 뉴스 캐시: 매시 15분, 25분, 35분
    for day_offset in range(2):
        target_date = now.date() + timedelta(days=day_offset)

        for hour in range(24):
            for minute in (15, 25, 35):
                schedules.append(
                    (
                        datetime(
                            target_date.year,
                            target_date.month,
                            target_date.day,
                            hour,
                            minute,
                            tzinfo=KST,
                        ),
                        "news",
                    )
                )

        # 일일 집계 캐시: Airflow 작업 완료를 고려해 20분 대기
        schedules.extend([
            (
                datetime(
                    target_date.year,
                    target_date.month,
                    target_date.day,
                    1, 50,
                    tzinfo=KST,
                ),
                "word-cloud",
            ),
            (
                datetime(
                    target_date.year,
                    target_date.month,
                    target_date.day,
                    3, 50,
                    tzinfo=KST,
                ),
                "sentiment",
            ),
            (
                datetime(
                    target_date.year,
                    target_date.month,
                    target_date.day,
                    4, 50,
                    tzinfo=KST,
                ),
                "keywords",
            ),
        ])

    return min(
        (schedule for schedule in schedules if schedule[0] > now),
        key=lambda schedule: schedule[0],
    )

async def run_cache_scheduler():
    logger.info("Cache scheduler started")

    while True:
        next_run, cache_prefix = get_next_cache_schedule()
        now = datetime.now(KST)

        wait_seconds = (next_run - now).total_seconds()

        logger.info(
            "Next cache invalidation: %s (%s)",
            next_run,
            cache_prefix,
        )

        await asyncio.sleep(wait_seconds)

        cache.invalidate(cache_prefix)

        logger.info(
            "Cache invalidated: %s",
            cache_prefix,
        )