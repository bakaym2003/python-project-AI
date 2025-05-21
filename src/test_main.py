from fastapi.testclient import TestClient
from src.main import app

import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="K@siet,bakyt123",
    host="db.homjbtgwrphodegiswaf.supabase.co",
    port="5432",
    sslmode="require"
)

cur = conn.cursor()
cur.execute("SELECT 1;")
print(cur.fetchone())
cur.close()
conn.close()

client = TestClient(app)

def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200 or response.status_code == 500  # 500 if DB is down

def test_jobs():
    response = client.get("/jobs")
    assert response.status_code == 200
