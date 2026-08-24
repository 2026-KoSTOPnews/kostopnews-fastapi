from datetime import date

from sqlalchemy import text

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.infrastructure.database import engine, get_db
from app.schema.company import CompanyResponse
from app.schema.keyword import KeywordsResponse, KeywordsRequest
from app.schema.news import NewsPageResponse
from app.schema.sentiment import SentimentRequest, SentimentResponse, CompanySentimentResponse
from app.service.company_service import get_companies
from app.service.keyword_service import extract_keywords_batch_service
from app.service.news_service import get_news_by_date
from app.service.sentiment_service import analyze_sentiment_batch_service, get_company_sentiment

app = FastAPI(title="News Sentiment API")

@app.get("/api/companies", response_model=list[CompanyResponse])
def read_companies(db: Session = Depends(get_db)):
    return get_companies(db)

@app.get("/api/companies/{company_id}/sentiment", response_model=CompanySentimentResponse)
def read_company_sentiment(company_id: int, target_date: date = Query(...), db: Session = Depends(get_db)):
    return get_company_sentiment(db, company_id, target_date)

@app.get("/api/companies/{company_id}/news", response_model=NewsPageResponse)
def read_today_news(company_id: int, target_date: date = Query(...), page: int = Query(1, ge=1), size: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)):
    return get_news_by_date(db, company_id, target_date, page, size)

@app.post("/sentiment/batch", response_model=list[SentimentResponse])
def batch_sentiment(reqs: list[SentimentRequest]):
    return analyze_sentiment_batch_service(reqs)

@app.post("/keywords/batch", response_model=list[KeywordsResponse])
def batch_keywords(reqs: list[KeywordsRequest]):
    return extract_keywords_batch_service(reqs)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/health/db")
def check_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"status": "ok"}
