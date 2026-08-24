from pydantic import BaseModel

class KeywordsRequest(BaseModel):
    article_id: int
    title: str
    content: str

class KeywordsResponse(BaseModel):
    article_id: int
    keywords: list[str]