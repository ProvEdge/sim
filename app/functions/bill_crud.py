from sqlalchemy.orm import Session

from .. import models
from database.schemas import bill_schema
def get_bills(db: Session, is_paid: bool = False, skip: int = 0, limit: int = 100):
    bills = db.query(models.Bill)
    bills = bills.filter(models.Bill.is_paid == is_paid)
    return bills.offset(skip).limit(limit).all()

def get_bill(db: Session, id: int):
    return db.query(models.Bill).filter(models.Bill.id == id).first()

# def get_clusters_by_group_id(db: Session, group_id: str):
#     return db.query(models.Cluster).filter(models.Cluster.group_id == group_id).all()

def create_bill(db: Session, bill: bill_schema.BillCreate):
    db_bill = models.Bill(
        usage_id=bill.usage_id,
        amount=bill.amount,
        currency=bill.currency,
        is_paid=bill.is_paid
    )
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

def edit_bill(db: Session, id: int, bill: bill_schema.BillEdit):
    attributes = {}
    for attr, value in bill.__dict__.items():
        if value is not None:
            attributes[attr] = value

    db.query(models.Bill).filter(models.Bill.id == id).update(attributes)
    db.commit()
    db_bill = get_bill(db, id)
    return db_bill

def delete_bill(db: Session, id: int):
    db_bill = get_bill(db, id)
    query_exec = db.query(models.Bill).filter(models.Bill.id == id).delete()
    db.commit()
    return db_bill