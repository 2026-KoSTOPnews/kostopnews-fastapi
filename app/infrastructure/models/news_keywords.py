from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsKeyword(Base):
    __tablename__ = "news_keywords"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    article_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("news_articles.id"),
        nullable=False,
    )
    keyword: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )