from typing import List

from fastapi import FastAPI

from app.schema.keyword import KeywordsResponse, KeywordsRequest
from app.schema.sentiment import SentimentRequest, SentimentResponse
from app.service.keyword_service import extract_keywords_batch_service
from app.service.sentiment_service import analyze_sentiment_batch_service

app = FastAPI(title="News Sentiment API")

@app.post("/sentiment/batch", response_model=List[SentimentResponse])
def batch_sentiment(reqs: List[SentimentRequest]):
    return analyze_sentiment_batch_service(reqs)

@app.post("/keywords/batch", response_model=List[KeywordsResponse])
def batch_keywords(reqs: List[KeywordsRequest]):
    return extract_keywords_batch_service(reqs)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
