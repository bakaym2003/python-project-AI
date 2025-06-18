# Job Applications API

A FastAPI-based REST API for managing job applications and job postings with OpenAI integration for generating job descriptions.

## Features

### Job Applications
- Create new job applications
- List all applications with optional filtering
- Get application details by candidate ID
- Update entire application
- Partially update application (email or job_id)
- Delete applications

### Job Postings
- Create new job postings
- List all job postings
- Get job posting by ID
- Update job postings
- Delete job postings
- Generate job descriptions using OpenAI GPT-4

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

3. Set up environment variables:
Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): http://127.0.0.1:8000/docs
- Alternative API documentation (ReDoc): http://127.0.0.1:8000/redoc

## API Endpoints

### Job Applications
- POST /applications - Create a new application
- GET /applications - List all applications (with optional email and company_name filters)
- GET /applications/{candidate_id} - Get application by candidate ID
- PUT /applications/{candidate_id} - Update entire application
- PATCH /applications/{candidate_id} - Partially update application
- DELETE /applications/{candidate_id} - Delete application

### Job Postings
- POST /jobs - Create a new job posting
- GET /jobs - List all job postings
- GET /jobs/{job_id} - Get job posting by ID
- PUT /jobs/{job_id} - Update job posting
- DELETE /jobs/{job_id} - Delete job posting
- POST /jobs/{job_id}/description - Generate job description using OpenAI

## OpenAI Integration

The API includes OpenAI integration for generating comprehensive job descriptions:
- Uses GPT-4 model
- Implements streaming responses
- Uses function calling for structured output
- Generates descriptions including responsibilities, requirements, and benefits

## Security

- Environment variables are used for sensitive information
- API keys are not stored in the codebase
- Input validation is implemented for all endpoints 