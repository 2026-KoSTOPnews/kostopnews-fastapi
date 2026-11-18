from datetime import datetime

from sqlalchemy import Integer, Text, Float, ForeignKey, TIMESTAMP, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsSentimentAggregate(Base):
    __tablename__ = "news_sentiment_aggregate"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "period_type",
            "period_start",
            name="news_sentiment_aggregate_unique",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    company_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
    )

    period_type: Mapped[str | None] = mapped_column(Text)
    period_start: Mapped[datetime | None] = mapped_column(TIMESTAMP)

    positive_count: Mapped[int | None] = mapped_column(Integer)
    negative_count: Mapped[int | None] = mapped_column(Integer)
    neutral_count: Mapped[int | None] = mapped_column(Integer)
    sentiment_score: Mapped[float | None] = mapped_column(Float)

    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
    )