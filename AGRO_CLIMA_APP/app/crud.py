from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from app.schemas import SensorUpdate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_sensor(db: Session, sensor: schemas.SensorCreate):
    db_sensor = models.Sensor(**sensor.model_dump())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

def get_sensores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sensor).offset(skip).limit(limit).all()

def get_sensor(db: Session, sensor_id: int):
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()

def delete_sensor(db: Session, sensor_id: int):
    sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()
    if sensor:
        db.delete(sensor)
        db.commit()
    return sensor
def update_sensor(db: Session, sensor_id: int, sensor_update: schemas.SensorUpdate):
    sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()
    if not sensor:
        return None

    for field, value in sensor_update.model_dump().items():
        setattr(sensor, field, value)
    
    db.commit()
    db.refresh(sensor)
    return sensor

    