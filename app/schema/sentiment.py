from datetime import datetime

from pydantic import BaseModel

class SentimentAggregateResponse(BaseModel):
    period_start: datetime
    positive_count: int
    negative_count: int
    neutral_count: int
    sentiment_score: float

class CompanySentimentResponse(BaseModel):
    daily: list[SentimentAggregateResponse]
    weekly: list[SentimentAggregateResponse]
    monthly: list[SentimentAggregateResponse]

class SentimentRequest(BaseModel):
    article_id: int
    company_id: int
    company_name: str
    title: str
    content: str

class SentimentResponse(BaseModel):
    article_id: int
    company_id: int
    summary: str
    sentiment: str
    score: float
    reason: str