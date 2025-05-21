from fastapi import FastAPI, Query, Path, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, Session


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


@app.get("/jobs")
def get_all_job_postings(db: Session = Depends(get_db)):
    result = db.execute(text('SELECT * FROM "JobPosting"'))
    rows = result.fetchall()

    output = []
    for row in rows:
                output.append(dict(row._mapping))  # добавляем каждую строку
    print("FINAL:", output)
    print("FINAL ROWS COUNT:", len(output))
    return output


