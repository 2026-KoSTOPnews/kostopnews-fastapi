from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsKeywordAggregate(Base):
    __tablename__ = "news_keyword_aggregate"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, nullable=False)
    period_type: Mapped[str] = mapped_column(String, nullable=False)
    period_start: Mapped[object] = mapped_column(TIMESTAMP, nullable=False)
    keyword: Mapped[str] = mapped_column(String, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)