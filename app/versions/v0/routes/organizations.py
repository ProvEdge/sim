from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Union

from app import models
from database.schemas import generic, organization_schema
from database.database import engine

from app.functions import organization_crud
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("", response_model=Union[organization_schema.ListOrganizationsResponse, generic.ResponseBase])
def read_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        orgs = organization_crud.get_organizations(db, skip=skip, limit=limit)
        return generate_response("SUCCESS", "Organizations are returned", orgs)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{id}", response_model=Union[organization_schema.GetOrganizationResponse, generic.ResponseBase])
def read_organization_by_id(id: int, db: Session = Depends(get_db)):
    try:
        db_org = organization_crud.get_organization(db, id=id)
        if db_org is None:
            return generate_response(
                "FAILURE",
                "No such an organization found"
            )
        return generate_response(
            "SUCCESS",
            "Organization is returned",
            db_org
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.get("/name/{name}", response_model=Union[organization_schema.GetOrganizationResponse, generic.ResponseBase])
def read_organization_by_name(name: str, db: Session = Depends(get_db)):
    try:
        db_org = organization_crud.get_organization_by_name(db, name=name)
        if db_org is None:
            return generate_response(
                "FAILURE",
                "No such an organization found"
            )
        return generate_response(
            "SUCCESS",
            "Organization is returned",
            db_org
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.post("", response_model=Union[organization_schema.GetOrganizationResponse, generic.ResponseBase])
def create_organization(org: organization_schema.OrganizationCreate, db: Session = Depends(get_db)):
    try:
        db_org = organization_crud.get_organization_by_name(db, name=org.name)

        if db_org:
            return generate_response(
                "FAILURE",
                "This organization exists"
            )
        
        org = organization_crud.create_organization(db=db, organization=org)

        return generate_response(
            "SUCCESS",
            "Organization is created",
            org
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.patch("/{id}", response_model=Union[organization_schema.GetOrganizationResponse, generic.ResponseBase])
def edit_organization(org: organization_schema.OrganizationCreate, id: int, db: Session = Depends(get_db)):
    try:
        db_org = organization_crud.get_organization(db, id=id)

        if not db_org:
            return generate_response(
                "FAILURE",
                "This organization does not exist"
            )
        
        org = organization_crud.edit_organization(db=db, organization=org, id=id)

        return generate_response(
            "SUCCESS",
            "Organization is edited",
            org
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.delete("/{id}", response_model=Union[organization_schema.GetOrganizationResponse, generic.ResponseBase])
def delete_organization(id: int, db: Session = Depends(get_db)):
    try:
        db_org = organization_crud.get_organization(db, id=id)
        if db_org is None:
            return generate_response(
                "FAILURE",
                "No such an organization found"
            )

        organization_crud.delete_organization(db, id=id)
        return generate_response(
            "SUCCESS",
            "Organization is deleted",
            db_org
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )