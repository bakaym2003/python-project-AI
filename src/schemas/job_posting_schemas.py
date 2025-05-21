# Pydantic for JobPosting
from pydantic import BaseModel

class JobPostingBase(BaseModel):
    title: str
    company_id: int
    compensation_min: float
    compensation_max: float
    location_type: str
    employment_type: str

class JobPostingCreate(JobPostingBase):
    pass

class JobPostingOut(JobPostingBase):
    id: int

    class Config:
        orm_mode = True