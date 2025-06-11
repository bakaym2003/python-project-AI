from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

app = FastAPI()

# In-memory storage for applications
applications = []

class ApplicationBase(BaseModel):
    candidate_id: str
    job_id: str
    email: str
    created_at: datetime = datetime.now()

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    email: Optional[str] = None
    job_id: Optional[str] = None

@app.post("/applications")
async def create_application(application: ApplicationCreate):
    applications.append(application)
    return {"message": "Application created successfully"}

@app.get("/applications")
async def get_applications(email: Optional[str] = None, job_id: Optional[str] = None):
    if email and job_id:
        return {"message": f"Applications for email {email} and job {job_id}"}
    elif email:
        return {"message": f"Applications for email {email}"}
    elif job_id:
        return {"message": f"Applications for job {job_id}"}
    return {"message": "All applications"}

@app.get("/applications/{candidate_id}")
async def get_application(candidate_id: str):
    for app in applications:
        if app.candidate_id == candidate_id:
            return {"message": f"Application found for candidate {candidate_id}"}
    raise HTTPException(status_code=404, detail="Application not found")

@app.put("/applications/{candidate_id}")
async def update_application(candidate_id: str, application: ApplicationCreate):
    for i, app in enumerate(applications):
        if app.candidate_id == candidate_id:
            applications[i] = application
            return {"message": "Application updated successfully"}
    raise HTTPException(status_code=404, detail="Application not found")

@app.patch("/applications/{candidate_id}")
async def partial_update_application(candidate_id: str, update: ApplicationUpdate):
    for app in applications:
        if app.candidate_id == candidate_id:
            if update.email:
                app.email = update.email
                return {"message": f"Email updated to {update.email}"}
            elif update.job_id:
                app.job_id = update.job_id
                return {"message": f"Job ID updated to {update.job_id}"}
    raise HTTPException(status_code=404, detail="Application not found")

@app.delete("/applications/{candidate_id}")
async def delete_application(candidate_id: str):
    for i, app in enumerate(applications):
        if app.candidate_id == candidate_id:
            applications.pop(i)
            return {"message": "Application deleted successfully"}
    raise HTTPException(status_code=404, detail="Application not found")