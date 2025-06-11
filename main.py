from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import uuid

app = FastAPI()

# In-memory storage for applications
applications = []

class ApplicationBase(BaseModel):
    candidate_id: str
    job_id: str
    email: EmailStr
    company_name: str
    created_at: datetime = datetime.now()

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    email: Optional[EmailStr] = None
    job_id: Optional[str] = None
    company_name: Optional[str] = None

class ApplicationResponse(BaseModel):
    message: str
    data: Optional[dict] = None

@app.post("/applications", response_model=ApplicationResponse)
async def create_application(application: ApplicationCreate):
    # Check if application already exists
    for app in applications:
        if app.candidate_id == application.candidate_id:
            raise HTTPException(
                status_code=400,
                detail="Application already exists for this candidate"
            )
    
    # Add new application
    applications.append(application)
    return ApplicationResponse(
        message="Application created successfully",
        data=application.dict()
    )

@app.get("/applications", response_model=ApplicationResponse)
async def get_applications(
    company_name: Optional[str] = None,
    email: Optional[EmailStr] = None
):
    filtered_apps = applications
    
    if company_name and email:
        filtered_apps = [
            app for app in applications
            if app.company_name == company_name and app.email == email
        ]
        return ApplicationResponse(
            message=f"Applications for company {company_name} and email {email}",
            data={"applications": [app.dict() for app in filtered_apps]}
        )
    elif company_name:
        filtered_apps = [
            app for app in applications
            if app.company_name == company_name
        ]
        return ApplicationResponse(
            message=f"Applications for company {company_name}",
            data={"applications": [app.dict() for app in filtered_apps]}
        )
    elif email:
        filtered_apps = [
            app for app in applications
            if app.email == email
        ]
        return ApplicationResponse(
            message=f"Applications for email {email}",
            data={"applications": [app.dict() for app in filtered_apps]}
        )
    
    return ApplicationResponse(
        message="All applications",
        data={"applications": [app.dict() for app in applications]}
    )

@app.get("/applications/{candidate_id}", response_model=ApplicationResponse)
async def get_application(candidate_id: str):
    for app in applications:
        if app.candidate_id == candidate_id:
            return ApplicationResponse(
                message=f"Application found for candidate {candidate_id}",
                data=app.dict()
            )
    raise HTTPException(
        status_code=404,
        detail=f"Application not found for candidate {candidate_id}"
    )

@app.put("/applications/{candidate_id}", response_model=ApplicationResponse)
async def update_application(candidate_id: str, application: ApplicationCreate):
    for i, app in enumerate(applications):
        if app.candidate_id == candidate_id:
            applications[i] = application
            return ApplicationResponse(
                message="Application updated successfully",
                data=application.dict()
            )
    raise HTTPException(
        status_code=404,
        detail=f"Application not found for candidate {candidate_id}"
    )

@app.patch("/applications/{candidate_id}", response_model=ApplicationResponse)
async def partial_update_application(candidate_id: str, update: ApplicationUpdate):
    for app in applications:
        if app.candidate_id == candidate_id:
            update_data = update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(app, field, value)
            
            updated_fields = ", ".join(update_data.keys())
            return ApplicationResponse(
                message=f"Updated fields: {updated_fields}",
                data=app.dict()
            )
    raise HTTPException(
        status_code=404,
        detail=f"Application not found for candidate {candidate_id}"
    )

@app.delete("/applications/{candidate_id}", response_model=ApplicationResponse)
async def delete_application(candidate_id: str):
    for i, app in enumerate(applications):
        if app.candidate_id == candidate_id:
            deleted_app = applications.pop(i)
            return ApplicationResponse(
                message="Application deleted successfully",
                data=deleted_app.dict()
            )
    raise HTTPException(
        status_code=404,
        detail=f"Application not found for candidate {candidate_id}"
    )