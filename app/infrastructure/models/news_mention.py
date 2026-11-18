from datetime import datetime

from sqlalchemy import Integer, Float, ForeignKey, TIMESTAMP, text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsMention(Base):
    __tablename__ = "news_mentions"

    __table_args__ = (
        UniqueConstraint(
            "article_id",
            "company_id",
            name="news_mentions_article_id_company_id_key",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    article_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("news_articles.id", ondelete="CASCADE"),
    )

    company_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        server_default=text("1.0"),
    )

    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
    )