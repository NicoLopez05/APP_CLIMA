from fastapi.testclient import TestClient
from app.main import app
#import pytest
client = TestClient(app)

# Datos de ejemplo
sensor_data = {
    "nombre": "Sensor X",
    "tipo": "Temperatura",
    "ubicacion": "Valle Norte",
    "activo": True,
    "alertas": False,
    "zona": "Norte",
    "cultivo": "Maíz"
}

sensor_update_data = {
    "nombre": "Sensor Actualizado",
    "tipo": "Humedad",
    "ubicacion": "Zona Sur",
    "zona": "Sur",
    "cultivo": "Papa"
}

def test_create_and_get_sensor():
    # Crear sensor
    response = client.post("/sensores/", json=sensor_data)
    assert response.status_code == 200
    sensor_id = response.json()["id"]

    # Obtener sensor por ID
    response = client.get(f"/sensores/{sensor_id}")
    assert response.status_code == 200
    assert response.json()["nombre"] == sensor_data["nombre"]

def test_update_sensor():
    # Crear sensor
    response = client.post("/sensores/", json=sensor_data)
    assert response.status_code == 200
    sensor_id = response.json()["id"]

    # Actualizar sensor
    response = client.put(f"/sensores/{sensor_id}", json=sensor_update_data)
    assert response.status_code == 200
    assert response.json()["nombre"] == sensor_update_data["nombre"]

def test_delete_sensor():
    # Crear sensor
    response = client.post("/sensores/", json=sensor_data)
    assert response.status_code == 200
    sensor_id = response.json()["id"]

    # Eliminar sensor
    response = client.delete(f"/sensores/{sensor_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

def test_get_sensor_not_found():
    response = client.get("/sensores/9999")
    assert response.status_code == 404

#@pytest.mark.xfail(reason="Validación de duplicados no implementada aún")
#def test_create_sensor_duplicado():
#    client.post("/sensores/", json=sensor_data)
#    response = client.post("/sensores/", json=sensor_data)
#    assert response.status_code == 400

def test_update_sensor_not_found():
    response = client.put("/sensores/9999", json=sensor_update_data)
    assert response.status_code == 404

def test_delete_sensor_not_found():
    response = client.delete("/sensores/9999")
    assert response.status_code == 404
def test_get_sensores():
    response = client.get("/sensores/")
    assert response.status_code == 200
