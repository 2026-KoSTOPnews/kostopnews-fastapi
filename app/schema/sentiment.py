from pydantic import BaseModel

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