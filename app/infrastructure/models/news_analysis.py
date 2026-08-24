from sqlalchemy import Float, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsAnalysis(Base):
    __tablename__ = "news_analysis"

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
    summary: Mapped[str | None] = mapped_column(Text)
    sentiment: Mapped[str] = mapped_column(Text, nullable=False)
    sentiment_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )