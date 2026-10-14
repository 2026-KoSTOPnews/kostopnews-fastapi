from collections.abc import Generator

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

class Base(DeclarativeBase):
    pass

def create_db_engine():
    return create_engine(
        settings.DATABASE_URL,
        pool_size=2,
        max_overflow=0,
        pool_pre_ping=True,
        pool_recycle=1800,
    )

def create_session_factory(engine):
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

def get_db(request: Request) -> Generator[Session, None, None]:
    db = request.app.state.SessionLocal()

    try:
        yield db
    finally:
        db.close()