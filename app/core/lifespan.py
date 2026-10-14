from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database import create_db_engine, create_session_factory
from app.infrastructure.llm.llm_client import create_llm_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_db_engine()
    llm_client = create_llm_client()

    app.state.engine = engine
    app.state.SessionLocal = create_session_factory(engine)
    app.state.llm_client = llm_client

    try:
        yield
    finally:
        llm_client.close()
        engine.dispose()