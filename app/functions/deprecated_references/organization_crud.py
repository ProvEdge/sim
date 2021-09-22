# from sqlalchemy.orm import Session

# from .. import models
# from database.schemas import organization_schema

# def get_organizations(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Organization).offset(skip).limit(limit).all()

# def get_organization(db: Session, id: int):
#     return db.query(models.Organization).filter(models.Organization.id == id).first()

# def get_organization_by_name(db: Session, name: str):
#     return db.query(models.Organization).filter(models.Organization.name == name).first()

# def create_organization(db: Session, organization: organization_schema.OrganizationCreate):
#     db_org = models.Organization(name=organization.name)
#     db.add(db_org)
#     db.commit()
#     db.refresh(db_org)
#     return db_org

# def edit_organization(db: Session, id: int, organization: organization_schema.OrganizationCreate):
#     db.query(models.Organization).filter(models.Organization.id == id).update(organization.dict())
#     db.commit()
#     db_org = db.query(models.Organization).filter(models.Organization.id == id).first()
#     return db_org

# def delete_organization(db: Session, id: int):
#     query_exec = db.query(models.Organization).filter(models.Organization.id == id).delete()
#     db.commit()
#     return query_exec