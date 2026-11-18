from datetime import datetime

from sqlalchemy import Integer, Text, TIMESTAMP, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str | None] = mapped_column(Text)
    link: Mapped[str | None] = mapped_column(Text, unique=True)
    pub_date: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    source: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str | None] = mapped_column(Text)

    company_extraction_processed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("FALSE"),
    )

    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
    )