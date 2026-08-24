from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.models.company import Company

def get_companies(db: Session) -> list[Company]:
    result = db.execute(
        select(Company)
        .order_by(Company.name)
    )

    return list(result.scalars().all())