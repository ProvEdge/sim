from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Union

from app import models
from database.schemas import generic, group_schema
from database.database import engine

from app.functions import keycloak_auth, keycloak_rest_crud
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

from keycloak import realm


@router.get("", response_model=Union[group_schema.GetGroupsResponse, generic.ResponseBase])
def get_keycloak_groups():
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        groups_req = keycloak_rest_crud.get_groups(admin_access_token=admin_access_token)
        if groups_req.status_code == 200: return generate_response(
            "SUCCESS",
            "Groups are returned",
            groups_req.data
        )
        else: return generate_response(
            "FAILURE",
            "Cannot get groups",
            groups_req.data
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



@router.get("/{id}/members", response_model=Union[dict, generic.ResponseBase])
def get_group_members(id: str):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        group_members = keycloak_rest_crud.get_group_members(admin_access_token=admin_access_token, id=id)
        return generate_response(
            "SUCCESS",
            "Group members are returned",
            group_members
        )
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))
