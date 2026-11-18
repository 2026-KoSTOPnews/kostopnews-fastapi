from datetime import datetime

from sqlalchemy import Integer, Text, ForeignKey, TIMESTAMP, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsKeywordAggregate(Base):
    __tablename__ = "news_keyword_aggregate"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "period_type",
            "period_start",
            "keyword",
            name="news_keyword_aggregate_unique",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    company_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
    )

    period_type: Mapped[str | None] = mapped_column(Text)
    period_start: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    keyword: Mapped[str | None] = mapped_column(Text)
    count: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
    )