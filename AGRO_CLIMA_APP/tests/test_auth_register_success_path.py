from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_success_path(tmp_path, monkeypatch):
    # registra un usuario nuevo para cubrir la rama "no existe" → create_user
    resp = client.post("/auth/register", json={
        "username": "cover_user",
        "password": "abcd12"
    })
    assert resp.status_code in (200, 201, 204, 202, 200)
