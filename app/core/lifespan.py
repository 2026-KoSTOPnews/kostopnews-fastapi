import asyncio

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.cache_scheduler import run_cache_scheduler

from app.infrastructure.database import Base, create_db_engine, create_session_factory
from app.infrastructure.llm.llm_client import create_llm_client

import app.infrastructure.models
from app.infrastructure.database_init import initialize_companies

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_db_engine()
    llm_client = create_llm_client()

    # 등록된 모델을 기준으로 없는 테이블 생성
    Base.metadata.create_all(bind=engine)
    initialize_companies(engine)

    app.state.engine = engine
    app.state.SessionLocal = create_session_factory(engine)
    app.state.llm_client = llm_client

    scheduler_task = asyncio.create_task(run_cache_scheduler())

    try:
        yield
    finally:
        scheduler_task.cancel()

        try:
            await scheduler_task
        except asyncio.CancelledError:
            pass

        llm_client.close()
        engine.dispose()