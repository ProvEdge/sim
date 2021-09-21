from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Union

from app import models
from database.schemas import generic, group_schema
from database.database import engine

from app.functions import organization_crud, keycloak_auth, keycloak_rest_crud
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

from keycloak import realm


@router.get("", response_model=Union[group_schema.GetGroupsResponse, generic.ResponseBase])
def get_keycloak_groups():
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        groups = keycloak_rest_crud.get_groups(admin_access_token=admin_access_token)
        return generate_response(
            "SUCCESS",
            "Groups are returned",
            groups
        )
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{id}", response_model=Union[group_schema.GetGroupResponse, generic.ResponseBase])
def get_keycloak_group(id: str):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        group = keycloak_rest_crud.get_group(admin_access_token=admin_access_token, id=id)
        return generate_response(
            "SUCCESS",
            "Group is returned",
            group
        )
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))
