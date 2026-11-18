from datetime import date

from pydantic import BaseModel

class WordCloudItem(BaseModel):
    word: str
    count: int

class WordCloudResponse(BaseModel):
    company_id: int
    period_type: str
    period_start: date
    period_end: date
    text_type: str
    words: list[WordCloudItem]