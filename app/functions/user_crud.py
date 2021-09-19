from sqlalchemy.orm import Session

from .. import models
from database.schemas import user_schema

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: user_schema.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def edit_user(db: Session, id: int, user: dict):
    db.query(models.User).filter(models.User.id == id).update(user)
    db.commit()
    db_user = db.query(models.User).filter(models.User.id == id).first()
    return db_user

def delete_user(db: Session, id: int):
    query_exec = db.query(models.User).filter(models.User.id == id).delete()
    db.commit()
    return query_exec