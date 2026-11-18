from datetime import datetime

from sqlalchemy import Integer, Text, ForeignKey, TIMESTAMP, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsKeyword(Base):
    __tablename__ = "news_keywords"

    __table_args__ = (
        UniqueConstraint(
            "article_id",
            "keyword",
            name="news_keywords_article_id_keyword_key",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    article_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("news_articles.id", ondelete="CASCADE"),
    )

    keyword: Mapped[str | None] = mapped_column(Text)
    model_version: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
    )