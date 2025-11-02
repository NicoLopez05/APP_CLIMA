from app import crud
from app.database import SessionLocal, Base, engine
from app.models import User

def test_crud_create_user_covers_hash_commit():
    # Asegura que la DB esté inicializada (por si el test corre aislado)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = crud.schemas.UserCreate(username="crud_user", password="abcd12")
        created = crud.create_user(db, user)
        assert created.username == "crud_user"
        # verifica que realmente quedó en DB
        row = db.query(User).filter(User.username == "crud_user").first()
        assert row is not None
    finally:
        db.close()
