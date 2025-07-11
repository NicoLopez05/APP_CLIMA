# app/models.py
from sqlalchemy import Column, Integer, String, Boolean

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Sensor(Base):
    __tablename__ = "sensores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo = Column(String)
    ubicacion = Column(String)
    activo = Column(Boolean, default=True)
    alertas = Column(Boolean, default=False)
    zona = Column(String)
    cultivo = Column(String)
