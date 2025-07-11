from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

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

    model_config = ConfigDict(from_attributes=True)

class SensorUpdate(BaseModel):
    nombre: str
    tipo: str
    ubicacion: str
    zona: str
    cultivo: str
