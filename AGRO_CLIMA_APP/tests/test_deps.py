# tests/test_deps.py
from app import deps

def test_get_db_generator():
    gen = deps.get_db()
    db = next(gen)
    assert db is not None
    gen.close()

