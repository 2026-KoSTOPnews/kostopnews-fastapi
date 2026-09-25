from datetime import datetime

from pydantic import BaseModel

class TodayNewsResponse(BaseModel):
    id: int
    title: str
    link: str
    pub_date: datetime

    summary: str | None
    sentiment: str | None
    sentiment_score: float | None

    keywords: list[str]

class NewsPageResponse(BaseModel):
    items: list[TodayNewsResponse]
    has_next: bool