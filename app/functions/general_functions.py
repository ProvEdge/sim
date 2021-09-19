from typing import Optional

def get_db():
    from database.database import SessionLocal, engine

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_response(status: str, message: str, data = {}):
    return {
        "status": status,
        "message": message,
        "data": data
    }