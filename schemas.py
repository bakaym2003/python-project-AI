from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Application Schemas
class ApplicationBase(BaseModel):
    candidate_id: str
    job_id: str
    email: EmailStr
    company_name: str

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    email: Optional[EmailStr] = None
    job_id: Optional[str] = None
    company_name: Optional[str] = None

class ApplicationResponse(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Job Posting Schemas
class JobPostingBase(BaseModel):
    title: str
    company: str
    location: str
    salary_range: Optional[str] = None
    description: Optional[str] = None

class JobPostingCreate(JobPostingBase):
    pass

class JobPostingUpdate(JobPostingBase):
    pass

class JobPostingResponse(JobPostingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Job Description Generation Schemas
class RequiredTools(BaseModel):
    tools: List[str]

class JobDescriptionRequest(BaseModel):
    required_tools: RequiredTools

class JobDescriptionResponse(BaseModel):
    message: str
    job_id: int
    description: str 