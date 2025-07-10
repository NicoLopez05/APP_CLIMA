import requests

def test_post_and_get_sensor():
    sensor = {
        "nombre": "test_sensor",
        "tipo": "lluvia",
        "ubicacion": "Test",
        "activo": True,
        "alertas": True,
        "zona": "Centro",
        "cultivo": "Maíz"
    }
    post_resp = requests.post("http://127.0.0.1:8000/sensores/", json=sensor)
    assert post_resp.status_code in [200, 201]

    get_resp = requests.get("http://127.0.0.1:8000/sensores/")
    assert get_resp.status_code == 200
