from pydantic import BaseModel

class CompanyResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }