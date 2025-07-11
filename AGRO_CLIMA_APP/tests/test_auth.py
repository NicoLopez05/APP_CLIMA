from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_fail():
    response = client.post("/auth/login", json={
        "username": "wrong",
        "password": "fail",
        "grant_type": "password"
    })
    assert response.status_code == 401

def test_login_success(monkeypatch):
    from app.routers import auth

    class DummyUser:
        username = "admin"
        hashed_password = "$2b$12$1234567890123456789012"  

    monkeypatch.setattr(auth.crud, "get_user_by_username", lambda db, username: DummyUser())
    monkeypatch.setattr(auth.crud.pwd_context, "verify", lambda plain, hashed: True)

    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "admin",
        "grant_type": "password"
    })
    assert response.status_code == 200
    assert response.json()["access_token"] == "fake-token"
    assert "access_token" in response.json()
    assert "token_type" in response.json()

def test_register_existing_user(monkeypatch):
    from app.routers import auth

    class DummyUser:
        username = "existing"

    def fake_get_user_by_username(db, username):
        return DummyUser()

    monkeypatch.setattr(auth.crud, "get_user_by_username", fake_get_user_by_username)

    response = client.post("/auth/register", json={
        "username": "existing",
        "password": "1234"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"
