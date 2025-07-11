# app/routers/sensores.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..deps import get_db

router = APIRouter()

@router.post("/", response_model=schemas.SensorOut)
def create(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    return crud.create_sensor(db, sensor)

@router.get("/", response_model=List[schemas.SensorOut])
def read_sensores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sensores(db, skip=skip, limit=limit)

@router.get("/{sensor_id}", response_model=schemas.SensorOut)
def read_sensor(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = crud.get_sensor(db, sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor

@router.delete("/{sensor_id}")
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)):
    sensor = crud.delete_sensor(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"ok": True}
    

@router.put("/{sensor_id}", response_model=schemas.SensorOut)
def update_sensor(sensor_id: int, sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    db_sensor = crud.get_sensor(db, sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    for key, value in sensor.dict().items():
        setattr(db_sensor, key, value)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

