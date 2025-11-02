from uuid import uuid4
from app import crud
from app.database import SessionLocal, Base, engine
from app.models import User

def test_crud_create_user_covers_hash_commit():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        unique_user = f"crud_user_{uuid4().hex[:8]}"
        payload = crud.schemas.UserCreate(username=unique_user, password="abcd12")
        created = crud.create_user(db, payload)
        assert created.username == unique_user
        row = db.query(User).filter(User.username == unique_user).first()
        assert row is not None
    finally:
        db.close()
