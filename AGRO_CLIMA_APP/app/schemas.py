# app/schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class SensorBase(BaseModel):
    nombre: str
    tipo: str
    ubicacion: str
    activo: bool = True
    alertas: bool = False
    zona: str
    cultivo: str

class SensorCreate(SensorBase):
    pass

class SensorOut(SensorBase):
    id: int
    class Config:
        orm_mode = True
class SensorUpdate(BaseModel):
    nombre: str
    tipo: str
    ubicacion: str
    zona: str
    cultivo: str