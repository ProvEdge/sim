# from sqlalchemy.orm import Session

# from .. import models
# from database.schemas import user_schema, org_user_schema

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

# def get_user(db: Session, id: int):
#     return db.query(models.User).filter(models.User.id == id).first()

# def get_user_by_name(db: Session, name: str):
#     return db.query(models.User).filter(models.User.name == name).first()

# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()

# def create_user(db: Session, user: user_schema.UserCreate):
#     db_user = models.User(name=user.name, email=user.email)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def edit_user(db: Session, id: int, user: dict):
#     db.query(models.User).filter(models.User.id == id).update(user)
#     db.commit()
#     db_user = db.query(models.User).filter(models.User.id == id).first()
#     return db_user

# def delete_user(db: Session, id: int):
#     query_exec = db.query(models.User).filter(models.User.id == id).delete()
#     db.commit()
#     return query_exec

# def join_organization(db: Session, participation: org_user_schema.OrgUser):
#     db_org_user = models.OrgUser(org_id=participation.org_id, user_id=participation.user_id)
#     db.add(db_org_user)
#     db.commit()
#     db.refresh(db_org_user)
#     return db_org_user

# def is_member(db: Session, participation: org_user_schema.OrgUser):
#     return db.query(models.OrgUser).filter(models.OrgUser.org_id == participation.org_id, models.OrgUser.user_id == participation.user_id).first()

# def get_users_organizations(db: Session, id: int):
#     return db.query(models.OrgUser).filter(models.OrgUser.user_id == id).all()

# def leave_organization(db: Session, participation: org_user_schema.OrgUser):
#     query_exec = db.query(models.OrgUser).filter(models.OrgUser.org_id == participation.org_id, models.OrgUser.user_id == participation.user_id).delete()
#     db.commit()
#     return query_exec