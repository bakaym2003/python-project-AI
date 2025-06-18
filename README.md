# Job Applications API

A FastAPI-based REST API for managing job applications and job postings with OpenAI integration for generating job descriptions. Built with a modular architecture and Supabase database integration.

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
- Generate job descriptions using OpenAI GPT-4 with required tools

### Database Integration
- Supabase PostgreSQL database
- SQLAlchemy ORM
- Automatic schema migrations
- Proper error handling and rollbacks

## Project Structure

```
├── main.py              # FastAPI application and endpoints
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic request/response schemas
├── database.py          # Database configuration and session management
├── openai_service.py    # OpenAI integration service
├── migrations.py        # Database migration scripts
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

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
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://username:password@host:port/database
```

4. Run database migrations:
```bash
python migrations.py
```

5. Run the application:
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

## Database Schema

### Job Postings Table
- id (SERIAL PRIMARY KEY)
- title (VARCHAR NOT NULL)
- company (VARCHAR NOT NULL)
- location (VARCHAR NOT NULL)
- salary_range (VARCHAR)
- description (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### Applications Table
- id (SERIAL PRIMARY KEY)
- candidate_id (VARCHAR NOT NULL UNIQUE)
- job_id (VARCHAR NOT NULL)
- email (VARCHAR NOT NULL)
- company_name (VARCHAR NOT NULL)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

## OpenAI Integration

The API includes OpenAI integration for generating comprehensive job descriptions:
- Uses GPT-4 model
- Implements streaming responses
- Uses function calling for structured output
- Accepts required_tools in the request body
- Generates descriptions including responsibilities, requirements, benefits, and required tools

### Example Job Description Request
```json
{
  "required_tools": {
    "tools": ["Python", "FastAPI", "PostgreSQL", "Docker"]
  }
}
```

## Code Quality Features

- **Modular Architecture**: Separated concerns into different modules
- **Type Safety**: Comprehensive type hints throughout
- **Error Handling**: Proper exception handling with rollbacks
- **Input Validation**: Pydantic models for request/response validation
- **Documentation**: Docstrings for all functions and classes
- **Database Transactions**: Proper transaction management
- **Environment Configuration**: Secure configuration management

## Security

- Environment variables for sensitive information
- API keys not stored in codebase
- Input validation on all endpoints
- SQL injection protection through SQLAlchemy
- Proper error handling without exposing sensitive data

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Database Migrations
```bash
# Run migrations
python migrations.py
```

### Code Formatting
```bash
# Install black
pip install black

# Format code
black .
``` 