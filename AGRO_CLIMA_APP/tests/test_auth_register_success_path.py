from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)

def test_register_success_path():
    unique_user = f"cover_user_{uuid4().hex[:8]}"
    resp = client.post("/auth/register", json={
        "username": unique_user,
        "password": "abcd12"
    })
    # Acepta cualquier 2xx
    assert 200 <= resp.status_code < 300, resp.text
