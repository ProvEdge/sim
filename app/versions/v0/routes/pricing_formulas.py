
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Union

from app import models
from database.schemas import generic, pricing_formula_schema
from database.database import engine

from app.functions import pricing_formula_crud
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("", response_model=Union[pricing_formula_schema.ListPricingFormulasResponse, generic.ResponseBase])
def read_pricing_formulas(robot_type: str = "", skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        pricing_formulas = pricing_formula_crud.get_pricing_formulas(db, robot_type=robot_type, skip=skip, limit=limit)
        return generate_response("SUCCESS", "Pricing formulas are returned", pricing_formulas)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{name}", response_model=Union[pricing_formula_schema.GetPricingFormulaResponse, generic.ResponseBase])
def read_pricing_formula_by_id(name: str, db: Session = Depends(get_db)):
    try:
        db_pricing_formula = pricing_formula_crud.get_pricing_formula(db, name=name)
        if db_pricing_formula is None:
            return generate_response(
                "FAILURE",
                "Pricing formula not found"
            )
        return generate_response(
            "SUCCESS",
            "Pricing formula is returned",
            db_pricing_formula
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.post("", response_model=Union[pricing_formula_schema.GetPricingFormulaResponse, generic.ResponseBase])
def create_pricing_formula(pricing_formula: pricing_formula_schema.PricingFormulaCreate, db: Session = Depends(get_db)):
    try:
        pf = pricing_formula_crud.create_pricing_formula(db=db, pricing_formula=pricing_formula)

        return generate_response(
            "SUCCESS",
            "Pricing formula is created",
            pf
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.patch("/{name}", response_model=Union[pricing_formula_schema.GetPricingFormulaResponse, generic.ResponseBase])
def edit_pricing_formula(pricing_formula: pricing_formula_schema.PricingFormulaEdit, name: str, db: Session = Depends(get_db)):
    try:
        db_pricing_formula = pricing_formula_crud.get_pricing_formula(db, name=name)

        if not db_pricing_formula:
            return generate_response(
                "FAILURE",
                "This pricing formula does not exist"
            )

        pf = pricing_formula_crud.edit_pricing_formula(db=db, pricing_formula=pricing_formula, name=name)

        return generate_response(
            "SUCCESS",
            "Pricing formula is edited",
            pf
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.delete("/{name}", response_model=Union[pricing_formula_schema.GetPricingFormulaResponse, generic.ResponseBase])
def delete_pricing_formula(name: str, db: Session = Depends(get_db)):
    try:
        db_pricing_formula = pricing_formula_crud.get_pricing_formula(db, name=name)
        if db_pricing_formula is None:
            return generate_response(
                "FAILURE",
                "Pricing formula not found"
            )

        delete_exec = pricing_formula_crud.delete_pricing_formula(db, name=name)
        return generate_response(
            "SUCCESS",
            "Pricing formula is deleted",
            delete_exec
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )