from app.main import app
from fastapi.testclient import TestClient

def test_main_loaded():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code in (200, 404)  