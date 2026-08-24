from sqlalchemy import Float, Integer, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsSentimentAggregate(Base):
    __tablename__ = "news_sentiment_aggregate"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, nullable=False)
    period_type: Mapped[str] = mapped_column(Text, nullable=False)
    period_start: Mapped[object] = mapped_column(TIMESTAMP, nullable=False)
    positive_count: Mapped[int] = mapped_column(Integer, nullable=False)
    negative_count: Mapped[int] = mapped_column(Integer, nullable=False)
    neutral_count: Mapped[int] = mapped_column(Integer, nullable=False)
    sentiment_score: Mapped[float] = mapped_column(Float, nullable=False)