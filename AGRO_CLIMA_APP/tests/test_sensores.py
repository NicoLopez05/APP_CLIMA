import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_get_all_sensores(client):
    response = client.get("/sensores/")
    assert response.status_code == 200

def test_create_sensor(client):
    payload = {
        "nombre": "Sensor Test",
        "tipo": "PH",
        "ubicacion": "Lote X",
        "zona": "Zona 1",
        "cultivo": "Café"
    }
    response = client.post("/sensores/", json=payload)
    assert response.status_code == 200
