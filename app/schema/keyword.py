from datetime import date
from pydantic import BaseModel

class KeywordItem(BaseModel):
    keyword: str
    count: int
    previous_count: int
    change: int

class KeywordAggregateResponse(BaseModel):
    period_start: date | None
    previous_period_start: date | None
    keywords: list[KeywordItem]

class CompanyKeywordResponse(BaseModel):
    daily: KeywordAggregateResponse
    weekly: KeywordAggregateResponse
    monthly: KeywordAggregateResponse

# class KeywordItem(BaseModel):
#     keyword: str
#     count: int
#
# class KeywordAggregateResponse(BaseModel):
#     period_start: date | None
#     keywords: list[KeywordItem]
#
# class CompanyKeywordResponse(BaseModel):
#     daily: KeywordAggregateResponse
#     weekly: KeywordAggregateResponse
#     monthly: KeywordAggregateResponse

class KeywordsRequest(BaseModel):
    article_id: int
    title: str
    content: str

class KeywordsResponse(BaseModel):
    article_id: int
    keywords: list[str]