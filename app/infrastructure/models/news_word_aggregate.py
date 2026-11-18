from datetime import date, datetime

from sqlalchemy import Integer, Text, Date, TIMESTAMP, ForeignKey, CheckConstraint, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsWordAggregate(Base):
    __tablename__ = "news_word_aggregate"

    __table_args__ = (
        CheckConstraint(
            "text_type IN ('title', 'content')",
            name="news_word_aggregate_text_type_check",
        ),
        UniqueConstraint(
            "company_id",
            "period_start",
            "text_type",
            "word",
            name="news_word_aggregate_unique",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
    )

    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    text_type: Mapped[str] = mapped_column(Text, nullable=False)
    word: Mapped[str] = mapped_column(Text, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
    )