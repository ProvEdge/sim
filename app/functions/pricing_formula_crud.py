from sqlalchemy.orm import Session

from .. import models
from database.schemas import pricing_formula_schema

def get_pricing_formulas(db: Session, robot_type: str = "", skip: int = 0, limit: int = 100):
    pricing_formulas = db.query(models.PricingFormula)
    if robot_type != "":
        pricing_formulas = pricing_formulas.filter(models.PricingFormula.robot_type == robot_type)
    return pricing_formulas.offset(skip).limit(limit).all()

def get_pricing_formula(db: Session, name: str):
    return db.query(models.PricingFormula).filter(models.PricingFormula.name == name).first()

# def get_clusters_by_group_id(db: Session, group_id: str):
#     return db.query(models.Cluster).filter(models.Cluster.group_id == group_id).all()

def create_pricing_formula(db: Session, pricing_formula: pricing_formula_schema.PricingFormulaCreate):
    db_pricing_formula = models.PricingFormula(
        name=pricing_formula.name,
        robot_type=pricing_formula.robot_type,
        robot_coefficient=pricing_formula.robot_coefficient,
        time_unit=pricing_formula.time_unit,
        amount_per_time_unit=pricing_formula.amount_per_time_unit,
        currency=pricing_formula.currency
    )
    db.add(db_pricing_formula)
    db.commit()
    db.refresh(db_pricing_formula)
    return db_pricing_formula

def edit_pricing_formula(db: Session, name: str, pricing_formula: pricing_formula_schema.PricingFormulaEdit):
    attributes = {}
    for attr, value in pricing_formula.__dict__.items():
        if value is not None:
            attributes[attr] = value

    db.query(models.PricingFormula).filter(models.PricingFormula.name == name).update(attributes)
    db.commit()
    if pricing_formula.name is not None:
        db_pricing_formula = get_pricing_formula(db, pricing_formula.name)
    else: db_pricing_formula = get_pricing_formula(db, name)
    return db_pricing_formula

def delete_pricing_formula(db: Session, name: str):
    db_pricing_formula = get_pricing_formula(db, id)
    query_exec = db.query(models.PricingFormula).filter(models.PricingFormula.name == name).delete()
    db.commit()
    return db_pricing_formula