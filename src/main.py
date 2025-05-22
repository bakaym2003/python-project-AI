from fastapi import FastAPI, Query, Path, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, Session
from src.schemas.company_schemas import CompanyOut, CompanyCreate
from src.schemas.job_posting_schemas import JobPostingOut, JobPostingCreate


# SQLAlchemy setup 
DATABASE_URL = "postgresql://postgres.zrkpwpogqmqpehcipfaf:Kasi3tBakyt987654321@aws-0-eu-north-1.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



app = FastAPI()

# This is our data model - what an application looks like
class Candidate(BaseModel):
    candidate_id: str 
    name: str 
    email: str 
    job_id: str | None = None

# This is our "database" - just a list in memory - cache memory
applications: List[Candidate] = []

#creating a db connection session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    
    
@app.get("/test")
def test_conn(db: Session = Depends(get_db)):
    return {"status": "ok"}

# Company endpoints
@app.get("/companies", response_model=List[CompanyOut])
def get_companies(db: Session = Depends(get_db)):
    result = db.execute(text('SELECT * FROM "Company"'))
    rows = result.fetchall()
    return [CompanyOut(**row._mapping) for row in rows]

@app.get("/companies/{company_id}", response_model=CompanyOut)
def get_company_by_id(company_id: int, db: Session = Depends(get_db)):
    result = db.execute(text('SELECT * FROM "Company" WHERE id = :id'), {"id": company_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Company not found")
    return CompanyOut(**result._mapping)

@app.post("/companies", response_model=CompanyOut)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    result = db.execute(
        text("""
            INSERT INTO "Company" (name, industry, url, headcount, country, state, city, is_public)
            VALUES (:name, :industry, :url, :headcount, :country, :state, :city, :is_public)
            RETURNING *
        """),
        company.dict()
    )
    db.commit()
    row = result.fetchone()
    return CompanyOut(**row._mapping)



@app.put("/companies/{company_id}", response_model=CompanyOut)
def update_company(company_id: int, updated_company: CompanyCreate, db: Session = Depends(get_db)):
    result = db.execute(
        text("""
            UPDATE "Company"
            SET name = :name,
                industry = :industry,
                url = :url,
                headcount = :headcount,
                country = :country,
                state = :state,
                city = :city,
                is_public = :is_public
            WHERE id = :company_id
            RETURNING *
        """),
        {**updated_company.dict(), "company_id": company_id}
    )
    db.commit()
    row = result.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return CompanyOut(**row._mapping)


@app.delete("/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text('DELETE FROM "Company" WHERE id = :company_id RETURNING id'),
        {"company_id": company_id}
    )
    db.commit()
    row = result.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": f"Company with id {company_id} deleted"}



# JobPosting endpoints
@app.get("/jobs", response_model=List[JobPostingOut])
def get_all_job_postings(db: Session = Depends(get_db)):
    result = db.execute(text('SELECT * FROM "JobPosting"'))
    rows = result.fetchall()
    return [JobPostingOut(**row._mapping) for row in rows]


@app.get("/jobs/{job_id}", response_model=JobPostingOut)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    result = db.execute(text('SELECT * FROM "JobPosting" WHERE id = :id'), {"id": job_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobPostingOut(**result._mapping)

@app.post("/jobs", response_model=JobPostingOut)
def create_job_posting(job: JobPostingCreate, db: Session = Depends(get_db)):
    result = db.execute(
        text("""
            INSERT INTO "JobPosting" (title, company_id, compensation_min, compensation_max, location_type, employment_type)
            VALUES (:title, :company_id, :compensation_min, :compensation_max, :location_type, :employment_type)
            RETURNING *
        """),
        job.dict()
    )
    db.commit()
    row = result.fetchone()
    return JobPostingOut(**row._mapping)



@app.put("/jobs/{job_id}", response_model=JobPostingOut)
def update_job_posting(job_id: int, updated_job: JobPostingCreate, db: Session = Depends(get_db)):
    result = db.execute(
        text("""
            UPDATE "JobPosting"
            SET title = :title,
                company_id = :company_id,
                compensation_min = :compensation_min,
                compensation_max = :compensation_max,
                location_type = :location_type,
                employment_type = :employment_type
            WHERE id = :job_id
            RETURNING *
        """),
        {**updated_job.dict(), "job_id": job_id}
    )
    db.commit()
    row = result.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobPostingOut(**row._mapping)



from fastapi import HTTPException

@app.delete("/jobs/{job_id}")
def delete_job_posting(job_id: int, db: Session = Depends(get_db)):
    result = db.execute(text('DELETE FROM "JobPosting" WHERE id = :job_id RETURNING id'), {"job_id": job_id})
    db.commit()
    row = result.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": f"Job with id {job_id} deleted"}

