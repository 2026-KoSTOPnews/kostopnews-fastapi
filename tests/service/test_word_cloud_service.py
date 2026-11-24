from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import text

from app.service.word_cloud_service import get_period_range, get_company_word_cloud


def create_test_company(db, suffix):
    return db.execute(
        text("""
            INSERT INTO companies (name, name_kr)
            VALUES (:name, :name_kr)
            RETURNING id
        """),
        {
            "name": f"test-company-{suffix}",
            "name_kr": f"테스트 기업 {suffix}",
        },
    ).scalar_one()


def insert_word(
    db,
    company_id,
    period_start,
    text_type,
    word,
    count,
):
    db.execute(
        text("""
            INSERT INTO news_word_aggregate (
                company_id,
                period_start,
                text_type,
                word,
                count
            )
            VALUES (
                :company_id,
                :period_start,
                :text_type,
                :word,
                :count
            )
        """),
        {
            "company_id": company_id,
            "period_start": period_start,
            "text_type": text_type,
            "word": word,
            "count": count,
        },
    )


@pytest.mark.parametrize(
    "period_type, target_date, expected_start, expected_end",
    [
        (
            "daily",
            date(2026, 11, 18),
            date(2026, 11, 18),
            date(2026, 11, 19),
        ),
        (
            "weekly",
            date(2026, 11, 18),
            date(2026, 11, 16),
            date(2026, 11, 23),
        ),
        (
            "monthly",
            date(2026, 11, 18),
            date(2026, 11, 1),
            date(2026, 12, 1),
        ),
        (
            "weekly",
            date(2027, 1, 1),
            date(2026, 12, 28),
            date(2027, 1, 4),
        ),
        (
            "monthly",
            date(2026, 12, 31),
            date(2026, 12, 1),
            date(2027, 1, 1),
        ),
    ],
)
def test_get_period_range(
    period_type,
    target_date,
    expected_start,
    expected_end,
):
    """기간 유형에 따라 조회 시작일과 종료일을 계산한다."""

    start_date, end_date = get_period_range(
        target_date,
        period_type,
    )

    assert start_date == expected_start
    assert end_date == expected_end


def test_get_period_range_invalid_type():
    """지원하지 않는 기간 유형이면 예외를 발생시킨다."""

    with pytest.raises(ValueError):
        get_period_range(
            date(2026, 11, 18),
            "yearly",
        )


def test_get_company_word_cloud_daily(real_db):
    """일간 워드 클라우드 데이터를 정상적으로 조회한다."""

    db = real_db
    suffix = uuid4().hex
    company_id = create_test_company(db, suffix)

    target_date = date(2026, 11, 18)

    insert_word(db, company_id, target_date, "title", "AI", 5)
    insert_word(db, company_id, target_date, "title", "반도체", 3)
    insert_word(db, company_id, target_date, "title", "실적", 2)

    insert_word(
        db,
        company_id,
        date(2026, 11, 17),
        "title",
        "AI",
        100,
    )

    result = get_company_word_cloud(
        db,
        company_id,
        target_date,
        "daily",
        "title",
        100,
    )

    assert result.company_id == company_id
    assert result.period_type == "daily"
    assert result.period_start == target_date
    assert result.period_end == target_date
    assert result.text_type == "title"

    assert [
        (item.word, item.count)
        for item in result.words
    ] == [
        ("AI", 5),
        ("반도체", 3),
        ("실적", 2),
    ]


@pytest.mark.parametrize(
    "period_type, expected_counts",
    [
        (
            "weekly",
            {
                "AI": 10,
                "반도체": 5,
                "실적": 2,
            },
        ),
        (
            "monthly",
            {
                "AI": 110,
                "반도체": 5,
                "실적": 2,
            },
        ),
    ],
)
def test_get_company_word_cloud_period_aggregation(
    real_db,
    period_type,
    expected_counts,
):
    """주간·월간 조회 시 일간 데이터를 단어별로 합산한다."""

    db = real_db
    suffix = uuid4().hex
    company_id = create_test_company(db, suffix)

    daily_data = [
        (date(2026, 11, 16), "AI", 2),
        (date(2026, 11, 16), "반도체", 1),
        (date(2026, 11, 17), "AI", 3),
        (date(2026, 11, 17), "반도체", 4),
        (date(2026, 11, 18), "AI", 5),
        (date(2026, 11, 18), "실적", 2),
        (date(2026, 11, 23), "AI", 100),
    ]

    for period_start, word, count in daily_data:
        insert_word(
            db,
            company_id,
            period_start,
            "title",
            word,
            count,
        )

    result = get_company_word_cloud(
        db,
        company_id,
        date(2026, 11, 18),
        period_type,
        "title",
        100,
    )

    actual_counts = {
        item.word: item.count
        for item in result.words
    }

    assert actual_counts == expected_counts


def test_get_company_word_cloud_filters_by_company(real_db):
    """다른 기업의 워드 클라우드 데이터는 조회하지 않는다."""

    db = real_db
    suffix = uuid4().hex

    company_id = create_test_company(db, f"{suffix}-1")
    other_company_id = create_test_company(db, f"{suffix}-2")

    target_date = date(2026, 11, 18)

    insert_word(
        db, company_id, target_date, "title", "AI", 5
    )
    insert_word(
        db, other_company_id, target_date, "title", "AI", 100
    )
    insert_word(
        db, other_company_id, target_date, "title", "반도체", 50
    )

    result = get_company_word_cloud(
        db,
        company_id,
        target_date,
        "daily",
        "title",
        100,
    )

    assert len(result.words) == 1
    assert result.words[0].word == "AI"
    assert result.words[0].count == 5


def test_get_company_word_cloud_filters_by_text_type(real_db):
    """제목과 본문 데이터를 구분하여 조회한다."""

    db = real_db
    suffix = uuid4().hex
    company_id = create_test_company(db, suffix)

    target_date = date(2026, 11, 18)

    insert_word(
        db, company_id, target_date, "title", "AI", 5
    )
    insert_word(
        db, company_id, target_date, "content", "AI", 20
    )
    insert_word(
        db, company_id, target_date, "content", "반도체", 10
    )

    result = get_company_word_cloud(
        db,
        company_id,
        target_date,
        "daily",
        "content",
        100,
    )

    actual_counts = {
        item.word: item.count
        for item in result.words
    }

    assert actual_counts == {
        "AI": 20,
        "반도체": 10,
    }


def test_get_company_word_cloud_limit(real_db):
    """요청한 개수만큼 상위 단어를 반환한다."""

    db = real_db
    suffix = uuid4().hex
    company_id = create_test_company(db, suffix)

    target_date = date(2026, 11, 18)

    for i in range(5):
        insert_word(
            db,
            company_id,
            target_date,
            "title",
            f"word-{i}",
            10 - i,
        )

    result = get_company_word_cloud(
        db,
        company_id,
        target_date,
        "daily",
        "title",
        3,
    )

    assert len(result.words) == 3
    assert [
        item.count for item in result.words
    ] == [10, 9, 8]


def test_get_company_word_cloud_empty(real_db):
    """조회 데이터가 없으면 빈 단어 목록을 반환한다."""

    db = real_db
    suffix = uuid4().hex
    company_id = create_test_company(db, suffix)

    result = get_company_word_cloud(
        db,
        company_id,
        date(2026, 11, 18),
        "daily",
        "title",
        100,
    )

    assert result.company_id == company_id
    assert result.words == []