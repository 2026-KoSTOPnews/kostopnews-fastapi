from fastapi import APIRouter, Request

from app.schema.keyword import KeywordsRequest, KeywordsResponse
from app.schema.sentiment import SentimentRequest, SentimentResponse
from app.service.keyword_service import extract_keywords_batch_service
from app.service.sentiment_service import analyze_sentiment_batch_service

router = APIRouter(tags=["Analysis"])

@router.post("/sentiment/batch", response_model=list[SentimentResponse])
async def batch_sentiment(reqs: list[SentimentRequest], request: Request):
    return await analyze_sentiment_batch_service(reqs, request)

@router.post("/keywords/batch", response_model=list[KeywordsResponse])
async def batch_keywords(reqs: list[KeywordsRequest], request: Request):
    return await extract_keywords_batch_service(reqs, request)