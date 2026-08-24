from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsMention(Base):
    __tablename__ = "news_mentions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("news_articles.id"),
        nullable=False,
    )
    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
    )