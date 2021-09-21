from fastapi import Depends, APIRouter
from pydantic.main import BaseModel
from sqlalchemy.orm import Session
from typing import Any, Union, List, Optional

from app import models
from database.schemas import generic, keycloak_schema, user_schema, org_user_schema
from database.database import engine

from app.functions import keycloak_rest_crud, user_crud, keycloak_auth
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("", response_model=Union[dict, generic.ResponseBase])
def get_keycloak_users():
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        users = keycloak_rest_crud.get_users(admin_access_token=admin_access_token)
        return users
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{id}", response_model=Union[dict, generic.ResponseBase])
def get_keycloak_users(id: str):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        user = keycloak_rest_crud.get_user(admin_access_token=admin_access_token, id=id)
        return user
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


class EditUser(BaseModel):
    email: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]


@router.put("/{id}", response_model=Union[dict, generic.ResponseBase])
def edit_keycloak_users(id: str, data: EditUser):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        edit_user_response = keycloak_rest_crud.edit_user(admin_access_token=admin_access_token, id=id, data=data)
        return generate_response(
            "SUCCESS",
            "User update request is sent to Keycloak server",
            {"update": edit_user_response}
        )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.delete("/{id}", response_model=Union[dict, generic.ResponseBase])
def delete_keycloak_users(id: str):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        delete_user_response = keycloak_rest_crud.delete_user(admin_access_token=admin_access_token, id=id)
        return generate_response(
            "SUCCESS",
            "User delete request is sent to Keycloak server",
            {"delete": delete_user_response}
        )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))
