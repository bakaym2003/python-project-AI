from sqlalchemy import text
from database import engine

def run_migrations():
    """Run database migrations"""
    with engine.connect() as connection:
        # Create job_postings table if it doesn't exist
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS job_postings (
                id SERIAL PRIMARY KEY,
                title VARCHAR NOT NULL,
                company VARCHAR NOT NULL,
                location VARCHAR NOT NULL,
                salary_range VARCHAR,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Create applications table if it doesn't exist
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS applications (
                id SERIAL PRIMARY KEY,
                candidate_id VARCHAR NOT NULL UNIQUE,
                job_id VARCHAR NOT NULL,
                email VARCHAR NOT NULL,
                company_name VARCHAR NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Add description column to job_postings if it doesn't exist
        try:
            connection.execute(text("""
                ALTER TABLE job_postings 
                ADD COLUMN IF NOT EXISTS description TEXT;
            """))
        except Exception as e:
            print(f"Description column might already exist: {e}")
        
        connection.commit()
        print("Database migrations completed successfully!")

if __name__ == "__main__":
    run_migrations() 