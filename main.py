from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

# Import our modules
from database import get_db, engine
from models import Base, JobPosting, Application
from schemas import (
    JobPostingCreate, JobPostingUpdate, JobPostingResponse,
    ApplicationCreate, ApplicationUpdate, ApplicationResponse,
    JobDescriptionRequest, JobDescriptionResponse
)
from openai_service import OpenAIService

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Applications API", version="1.0.0")

# Initialize OpenAI service
try:
    openai_service = OpenAIService()
except ValueError as e:
    print(f"Warning: OpenAI service not initialized: {e}")
    openai_service = None

# Application Endpoints
@app.post("/applications", response_model=ApplicationResponse)
async def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Create a new job application"""
    try:
        # Check if application already exists
        existing_app = db.query(Application).filter(
            Application.candidate_id == application.candidate_id
        ).first()
        
        if existing_app:
            raise HTTPException(
                status_code=400,
                detail="Application already exists for this candidate"
            )
        
        # Create new application
        db_application = Application(**application.dict())
        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        
        return ApplicationResponse.from_orm(db_application)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/applications", response_model=List[ApplicationResponse])
async def get_applications(
    company_name: str = None,
    email: str = None,
    db: Session = Depends(get_db)
):
    """Get applications with optional filtering"""
    try:
        query = db.query(Application)
        
        if company_name and email:
            query = query.filter(
                Application.company_name == company_name,
                Application.email == email
            )
        elif company_name:
            query = query.filter(Application.company_name == company_name)
        elif email:
            query = query.filter(Application.email == email)
        
        applications = query.all()
        return [ApplicationResponse.from_orm(app) for app in applications]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/applications/{candidate_id}", response_model=ApplicationResponse)
async def get_application(candidate_id: str, db: Session = Depends(get_db)):
    """Get application by candidate ID"""
    try:
        application = db.query(Application).filter(
            Application.candidate_id == candidate_id
        ).first()
        
        if not application:
            raise HTTPException(
                status_code=404,
                detail=f"Application not found for candidate {candidate_id}"
            )
        
        return ApplicationResponse.from_orm(application)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/applications/{candidate_id}", response_model=ApplicationResponse)
async def update_application(
    candidate_id: str,
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Update an entire application"""
    try:
        db_application = db.query(Application).filter(
            Application.candidate_id == candidate_id
        ).first()
        
        if not db_application:
            raise HTTPException(
                status_code=404,
                detail=f"Application not found for candidate {candidate_id}"
            )
        
        # Update fields
        for key, value in application.dict().items():
            setattr(db_application, key, value)
        
        db.commit()
        db.refresh(db_application)
        
        return ApplicationResponse.from_orm(db_application)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/applications/{candidate_id}", response_model=ApplicationResponse)
async def partial_update_application(
    candidate_id: str,
    update: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    """Partially update an application"""
    try:
        db_application = db.query(Application).filter(
            Application.candidate_id == candidate_id
        ).first()
        
        if not db_application:
            raise HTTPException(
                status_code=404,
                detail=f"Application not found for candidate {candidate_id}"
            )
        
        # Update only provided fields
        update_data = update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_application, field, value)
        
        db.commit()
        db.refresh(db_application)
        
        return ApplicationResponse.from_orm(db_application)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/applications/{candidate_id}")
async def delete_application(candidate_id: str, db: Session = Depends(get_db)):
    """Delete an application"""
    try:
        db_application = db.query(Application).filter(
            Application.candidate_id == candidate_id
        ).first()
        
        if not db_application:
            raise HTTPException(
                status_code=404,
                detail=f"Application not found for candidate {candidate_id}"
            )
        
        db.delete(db_application)
        db.commit()
        
        return {"message": "Application deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Job Posting Endpoints
@app.post("/jobs", response_model=JobPostingResponse)
async def create_job_posting(
    job: JobPostingCreate,
    db: Session = Depends(get_db)
):
    """Create a new job posting"""
    try:
        db_job = JobPosting(**job.dict())
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        
        return JobPostingResponse.from_orm(db_job)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs", response_model=List[JobPostingResponse])
async def get_job_postings(db: Session = Depends(get_db)):
    """Get all job postings"""
    try:
        jobs = db.query(JobPosting).all()
        return [JobPostingResponse.from_orm(job) for job in jobs]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs/{job_id}", response_model=JobPostingResponse)
async def get_job_posting(job_id: int, db: Session = Depends(get_db)):
    """Get a specific job posting by ID"""
    try:
        job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job posting not found")
        
        return JobPostingResponse.from_orm(job)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/jobs/{job_id}", response_model=JobPostingResponse)
async def update_job_posting(
    job_id: int,
    job: JobPostingUpdate,
    db: Session = Depends(get_db)
):
    """Update a job posting"""
    try:
        db_job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        
        if not db_job:
            raise HTTPException(status_code=404, detail="Job posting not found")
        
        # Update fields
        for key, value in job.dict().items():
            setattr(db_job, key, value)
        
        db.commit()
        db.refresh(db_job)
        
        return JobPostingResponse.from_orm(db_job)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/jobs/{job_id}")
async def delete_job_posting(job_id: int, db: Session = Depends(get_db)):
    """Delete a job posting"""
    try:
        db_job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        
        if not db_job:
            raise HTTPException(status_code=404, detail="Job posting not found")
        
        db.delete(db_job)
        db.commit()
        
        return {"message": "Job posting deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/jobs/{job_id}/description", response_model=JobDescriptionResponse)
async def generate_job_description(
    job_id: int,
    request: JobDescriptionRequest,
    db: Session = Depends(get_db)
):
    """Generate job description using OpenAI GPT model with required tools"""
    if not openai_service:
        raise HTTPException(
            status_code=500,
            detail="OpenAI service not available"
        )
    
    try:
        # Find the job posting
        job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job posting not found")
        
        # Generate description using OpenAI
        job_data = {
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "salary_range": job.salary_range
        }
        
        required_tools = request.required_tools.tools
        generated_description = openai_service.generate_job_description(
            job_data, required_tools
        )
        
        # Update the job posting with the generated description
        job.description = generated_description
        db.commit()
        db.refresh(job)
        
        return JobDescriptionResponse(
            message="Job description generated successfully",
            job_id=job_id,
            description=generated_description
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))