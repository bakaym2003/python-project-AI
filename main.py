from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from openai import OpenAI
import os
import json

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

# Job Posting Models
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

# In-memory storage for job postings
job_postings = []
job_id_counter = 1

# OpenAI Function Definition
def get_job_description_function():
    return {
        "name": "generate_job_description",
        "description": "Generate a comprehensive job description based on job details",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "A comprehensive job description including responsibilities, requirements, and benefits"
                }
            },
            "required": ["description"]
        }
    }

@app.post("/applications", response_model=ApplicationResponse)
async def create_application(application: ApplicationCreate):
    """Create a new job application"""
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
    """Get applications with optional filtering"""
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
    """Get application by candidate ID"""
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
    """Update an entire application"""
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
    """Partially update an application"""
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
    """Delete an application"""
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

# Job Posting Endpoints
@app.post("/jobs", response_model=JobPostingResponse)
async def create_job_posting(job: JobPostingCreate):
    """Create a new job posting"""
    global job_id_counter
    job_dict = job.dict()
    job_dict["id"] = job_id_counter
    job_dict["created_at"] = datetime.now()
    job_postings.append(job_dict)
    job_id_counter += 1
    return JobPostingResponse(**job_dict)

@app.get("/jobs", response_model=List[JobPostingResponse])
async def get_job_postings():
    """Get all job postings"""
    return [JobPostingResponse(**job) for job in job_postings]

@app.get("/jobs/{job_id}", response_model=JobPostingResponse)
async def get_job_posting(job_id: int):
    """Get a specific job posting by ID"""
    for job in job_postings:
        if job["id"] == job_id:
            return JobPostingResponse(**job)
    raise HTTPException(status_code=404, detail="Job posting not found")

@app.put("/jobs/{job_id}", response_model=JobPostingResponse)
async def update_job_posting(job_id: int, job: JobPostingUpdate):
    """Update a job posting"""
    for i, existing_job in enumerate(job_postings):
        if existing_job["id"] == job_id:
            job_dict = job.dict()
            job_dict["id"] = job_id
            job_dict["created_at"] = existing_job["created_at"]
            job_postings[i] = job_dict
            return JobPostingResponse(**job_dict)
    raise HTTPException(status_code=404, detail="Job posting not found")

@app.delete("/jobs/{job_id}")
async def delete_job_posting(job_id: int):
    """Delete a job posting"""
    for i, job in enumerate(job_postings):
        if job["id"] == job_id:
            job_postings.pop(i)
            return {"message": "Job posting deleted successfully"}
    raise HTTPException(status_code=404, detail="Job posting not found")

@app.post("/jobs/{job_id}/description")
async def generate_job_description(job_id: int):
    """Generate job description using OpenAI GPT model"""
    # Find the job posting
    job = None
    for existing_job in job_postings:
        if existing_job["id"] == job_id:
            job = existing_job
            break
    
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    try:
        # Prepare the prompt for OpenAI
        prompt = f"""
        Generate a comprehensive job description for the following position:
        
        Title: {job['title']}
        Company: {job['company']}
        Location: {job['location']}
        Salary Range: {job.get('salary_range', 'Not specified')}
        
        Please include:
        1. Job overview
        2. Key responsibilities
        3. Required qualifications
        4. Preferred qualifications
        5. Benefits and perks
        6. Company culture information
        """
        
        # Call OpenAI API with function calling
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional HR specialist who creates compelling and comprehensive job descriptions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            functions=[get_job_description_function()],
            function_call={"name": "generate_job_description"},
            stream=True
        )
        
        # Process streaming response
        full_description = ""
        for chunk in response:
            if chunk.choices[0].delta.function_call:
                function_call = chunk.choices[0].delta.function_call
                if function_call.arguments:
                    full_description += function_call.arguments
        
        # Parse the function call arguments
        try:
            description_data = json.loads(full_description)
            generated_description = description_data.get("description", "")
        except json.JSONDecodeError:
            # Fallback: use the raw response
            generated_description = full_description
        
        # Update the job posting with the generated description
        for i, existing_job in enumerate(job_postings):
            if existing_job["id"] == job_id:
                job_postings[i]["description"] = generated_description
                break
        
        return {
            "message": "Job description generated successfully",
            "job_id": job_id,
            "description": generated_description
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating job description: {str(e)}"
        )