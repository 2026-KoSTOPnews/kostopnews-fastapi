from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.cache import cache

from app.infrastructure.database import get_db
from app.schema.company import CompanyResponse
from app.service.company_service import get_companies

router = APIRouter(prefix="/api/companies", tags=["Company"])

@router.get("", response_model=list[CompanyResponse])
def read_companies(db: Session = Depends(get_db)):
    cache_key = ("companies",)

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    result = get_companies(db)
    cache.set(cache_key, result, ttl=86400)

    return result