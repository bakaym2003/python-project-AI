# Job Applications API

A FastAPI-based REST API for managing job applications.

## Features

- Create new job applications
- List all applications with optional filtering
- Get application details by candidate ID
- Update entire application
- Partially update application (email or job_id)
- Delete applications

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): http://127.0.0.1:8000/docs
- Alternative API documentation (ReDoc): http://127.0.0.1:8000/redoc

## API Endpoints

- POST /applications - Create a new application
- GET /applications - List all applications (with optional email and job_id filters)
- GET /applications/{candidate_id} - Get application by candidate ID
- PUT /applications/{candidate_id} - Update entire application
- PATCH /applications/{candidate_id} - Partially update application
- DELETE /applications/{candidate_id} - Delete application 