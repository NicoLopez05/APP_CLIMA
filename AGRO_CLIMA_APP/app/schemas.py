# app/schemas.py
from pydantic import BaseModel, Field, ConfigDict

# ===== Usuarios =====
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=4, max_length=256)

class UserOut(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)  # ← sin warnings

# ===== Sensores =====
class SensorBase(BaseModel):
    nombre: str
    tipo: str
    ubicacion: str
    activo: bool = True
    alertas: bool = False
    zona: str | None = None
    cultivo: str | None = None

class SensorCreate(SensorBase):
    pass

class SensorUpdate(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    ubicacion: str | None = None
    activo: bool | None = None
    alertas: bool | None = None
    zona: str | None = None
    cultivo: str | None = None

class SensorOut(SensorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  # ← sin warnings
