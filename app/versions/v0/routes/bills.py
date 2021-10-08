
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, Union

from app import models
from database.schemas import generic, bill_schema
from database.database import engine

from app.functions import bill_crud
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("", response_model=Union[bill_schema.ListBillsResponse, generic.ResponseBase])
def read_bills(is_paid: bool = False, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        bills = bill_crud.get_bills(db, is_paid=is_paid, skip=skip, limit=limit)
        return generate_response("SUCCESS", "Bills are returned", bills)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{id}", response_model=Union[bill_schema.GetBillResponse, generic.ResponseBase])
def read_bill_by_id(id: int, db: Session = Depends(get_db)):
    try:
        db_bill = bill_crud.get_bill(db, id=id)
        if db_bill is None:
            return generate_response(
                "FAILURE",
                "Bill not found"
            )
        return generate_response(
            "SUCCESS",
            "Bill is returned",
            db_bill
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

# # @router.get("/name/{name}", response_model=Union[organization_schema.GetOrganizationResponse, generic.ResponseBase])
# # def read_organization_by_name(name: str, db: Session = Depends(get_db)):
# #     try:
# #         db_org = organization_crud.get_organization_by_name(db, name=name)
# #         if db_org is None:
# #             return generate_response(
# #                 "FAILURE",
# #                 "No such an organization found"
# #             )
# #         return generate_response(
# #             "SUCCESS",
# #             "Organization is returned",
# #             db_org
# #         )
# #     except Exception as e:
# #         return generate_response(
# #             "FAILURE",
# #             str(e)
# #         )

@router.post("", response_model=Union[bill_schema.GetBillResponse, generic.ResponseBase])
def create_bill(bill: bill_schema.BillCreate, db: Session = Depends(get_db)):
    try:
        new_bill = bill_crud.create_bill(db=db, bill=bill)

        return generate_response(
            "SUCCESS",
            "Bill is created",
            new_bill
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.patch("/{id}", response_model=Union[bill_schema.GetBillResponse, generic.ResponseBase])
def edit_bill(bill: bill_schema.BillEdit, id: int, db: Session = Depends(get_db)):
    try:
        db_bill = bill_crud.get_bill(db, id=id)

        if not db_bill:
            return generate_response(
                "FAILURE",
                "This bill does not exist"
            )

        edit_bill = bill_crud.edit_bill(db=db, bill=bill, id=id)

        return generate_response(
            "SUCCESS",
            "Bill is edited",
            edit_bill
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.delete("/{id}", response_model=Union[bill_schema.GetBillResponse, generic.ResponseBase])
def delete_bill(id: int, db: Session = Depends(get_db)):
    try:
        db_bill = bill_crud.get_bill(db, id=id)
        if db_bill is None:
            return generate_response(
                "FAILURE",
                "Bill not found"
            )

        delete_exec = bill_crud.delete_bill(db, id=id)
        return generate_response(
            "SUCCESS",
            "Bill is deleted",
            delete_exec
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )