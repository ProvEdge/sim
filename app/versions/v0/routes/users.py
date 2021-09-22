from fastapi import Depends, APIRouter
from pydantic.main import BaseModel
from sqlalchemy.orm import Session
from typing import Any, Union, List, Optional

from app import models
from database.schemas import generic, group_schema, user_schema
from database.database import engine

from app.functions import keycloak_rest_crud, keycloak_auth
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("", response_model=Union[user_schema.GetUsersResponse, generic.ResponseBase])
def get_keycloak_users():
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        users_req = keycloak_rest_crud.get_users(admin_access_token=admin_access_token)
        if users_req.status_code == 200: return generate_response(
            "SUCCESS",
            "Users are returned",
            users_req.data
        )
        else: return generate_response(
            "FAILURE",
            "Cannot get users",
            users_req.data
        )
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{id}", response_model=Union[user_schema.GetUserResponse, generic.ResponseBase])
def get_keycloak_user(id: str):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        user_req = keycloak_rest_crud.get_user(admin_access_token=admin_access_token, id=id)
        if user_req.status_code == 200:
            return generate_response(
                "SUCCESS",
                "User is returned",
                user_req.data
            )
        else: return generate_response(
            "FAILURE",
            "Cannot get user",
            user_req.data
        )
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.put("/{id}", response_model=Union[user_schema.GetUserResponse, generic.ResponseBase])
def edit_keycloak_users(id: str, data: user_schema.EditUserRequest):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        edit_user_req = keycloak_rest_crud.edit_user(admin_access_token=admin_access_token, id=id, data=data)
        if edit_user_req.status_code == 204: return generate_response(
            "SUCCESS",
            "User is updated",
            edit_user_req.data
        )
        else: return generate_response(
            "FAILURE",
            "Cannot update user",
            edit_user_req.data
        )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))



@router.delete("/{id}", response_model=Union[user_schema.GetUserResponse, generic.ResponseBase])
def delete_keycloak_user(id: str):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        delete_user_req = keycloak_rest_crud.delete_user(admin_access_token=admin_access_token, id=id)
        if delete_user_req.status_code == 204: return generate_response(
            "SUCCESS",
            "User is deleted",
            delete_user_req.data
        )
        else: return generate_response(
            "FAILURE",
            "Cannot delete user",
            delete_user_req.data
        )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{id}/groups", response_model=Union[group_schema.GetGroupsResponse, generic.ResponseBase])
def get_users_groups(id: str):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        groups_req = keycloak_rest_crud.get_users_groups(admin_access_token=admin_access_token, id=id)
        if groups_req.status_code == 200: return generate_response(
            "SUCCESS",
            "User's groups are returned",
            groups_req.data
        )
        else: return generate_response(
            "FAILURE",
            "Cannot get user's groups",
            groups_req.data
        )
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{id}/attributes", response_model=Union[user_schema.GetUserAttributesResponse, generic.ResponseBase])
def get_user_attributes(id: str):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        attributes_req = keycloak_rest_crud.get_user_attributes(admin_access_token=admin_access_token, id=id)
        if attributes_req.status_code == 200: return generate_response(
            "SUCCESS",
            "User's attributes are returned",
            attributes_req.data
        )
        else: return generate_response(
            "FAILURE",
            "Cannot get user's attributes",
            attributes_req.data
        )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))