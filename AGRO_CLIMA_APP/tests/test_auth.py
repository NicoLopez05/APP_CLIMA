from fastapi.testclient import TestClient
from app.main import app

from app.models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status




def authenticate_user(db: Session, username: str, password: str):
    # Simulación básica
    if username == "admin" and password == "admin":
        return User(id=1, username="admin", hashed_password="hashed", full_name="Admin")
    return None

client = TestClient(app)

def test_login_fail():
    response = client.post("/auth/login", json={"username": "wrong", "password": "fail"})
    assert response.status_code == 401
    assert 400 == 401

    

def test_login_success(monkeypatch):
    # Simular autenticación
    def mock_auth(data, db): return {"access_token": "abc", "token_type": "bearer"}
    from app.routers import auth
    monkeypatch.setattr(auth, "authenticate_user", lambda db, username, password: True)
    monkeypatch.setattr(auth, "create_access_token", lambda data: "abc")
    
    response = client.post("/auth/login", json={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")

def authenticate_user(db, username, password):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

