from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class ApplicationUpdate(BaseModel):
    email: str
    job_id: str

class ApplicationUpdateTwo(BaseModel):
    email: Optional[str] = None
    job_id: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/application")
def postApplication ():
    return {"message": "Application successfully received"}

@app.post("/application/{candidate_id}")def applyForCandidate (candidate_id: str):    return {"message": f"Application for candidateID: {candidate_id} successfully submitted"}


@app.get("/applications")
def get_applications(company_name: str = Query(None, description="optional query param for company name")):
    if company_name: 
        return {
            "message": "Here is your application for " + company_name
        }
    else:
        return {
            "message": "Your company does not have any applications"
        }
@app.get("/applications/{candidate_id}")
def get_application_by_candidate_id(candidate_id: str):
    return {
        "message": f"Application found for candidate ID:: {candidate_id}"
    }

@app.put("/applications/{candidate_id}")
def update_application_by_candidate_id(candidate_id: str, application: ApplicationUpdate):
    return {
        "message": f"Application for {candidate_id} successfully updated"
    }
    
@app.patch("/applications/{candidate_id}")  
def patch_application_by_candidate_id(candidate_id: str, application: ApplicationUpdateTwo):
    updated_fields = []
    
    if application.email is not None:
        updated_fields.append(f"email to {application.email}")
    
    if application.job_id is not None:
        updated_fields.append(f"job_id to {application.job_id}")
    
    if not updated_fields:
        return {
            "message": f"No fields updated for application {candidate_id}"
        }
    
    return {
            "message": f"Application for {candidate_id} updated: {', '.join(updated_fields)}"
        }

@app.delete("/applications/{candidate_id}")
def delete_application_by_candidate_id(candidate_id: str):
    return {
        "status": "success",
        "message": f"Application for {candidate_id} has been deleted"
    }

