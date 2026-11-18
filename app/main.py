from fastapi import Request
from sqlalchemy import text

from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.router import company_router, analysis_router, news_router, word_cloud_router

app = FastAPI(lifespan=lifespan, title="News Sentiment API")

app.include_router(company_router.router)
app.include_router(news_router.router)
app.include_router(analysis_router.router)
app.include_router(word_cloud_router.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/health/db")
def check_db(request: Request):
    engine = request.app.state.engine

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"status": "ok"}
