def parse_tipo_sensor(tipo):
    return tipo.upper()

def test_parse_tipo_sensor():
    assert parse_tipo_sensor("lluvia") == "LLUVIA"
