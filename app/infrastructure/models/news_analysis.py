from datetime import datetime

from sqlalchemy import Integer, Text, Float, ForeignKey, TIMESTAMP, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsAnalysis(Base):
    __tablename__ = "news_analysis"

    __table_args__ = (
        UniqueConstraint(
            "article_id",
            "company_id",
            name="news_analysis_article_company_unique",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    article_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("news_articles.id", ondelete="CASCADE"),
        nullable=False,
    )

    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(Text)
    sentiment: Mapped[str | None] = mapped_column(Text)
    sentiment_score: Mapped[float | None] = mapped_column(Float)
    model_version: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
    )