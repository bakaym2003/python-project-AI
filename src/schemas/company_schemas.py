# Pydantic for Company
from pydantic import BaseModel

class CompanyBase(BaseModel):
    name: str
    industry: str
    url: str
    headcount: int
    country: str
    state: str
    city: str
    is_public: bool

class CompanyCreate(CompanyBase):
    pass

class CompanyOut(CompanyBase):
    id: int

    class Config:
        orm_mode = True