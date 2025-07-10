import pytest
from pydantic import ValidationError, BaseModel

class Sensor(BaseModel):
    nombre: str
    tipo: str
    activo: bool

def test_missing_fields():
    with pytest.raises(ValidationError):
        Sensor(nombre="Sensor 1")
