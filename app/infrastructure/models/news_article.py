from datetime import datetime

from sqlalchemy import Integer, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    link: Mapped[str] = mapped_column(Text, nullable=False)
    pub_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)