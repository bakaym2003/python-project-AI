from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_delete_application():
    """Test deleting an application."""
    candidate_id = "abc123"
    response = client.delete(f"/applications/{candidate_id}")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": f"Application for {candidate_id} has been deleted"
    } 