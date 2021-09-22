from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Union, Optional

from app import models
from database.schemas import generic, group_schema, user_schema
from database.database import engine

from app.functions import keycloak_auth, keycloak_rest_crud
from app.functions.general_functions import generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("", response_model=Union[group_schema.GetGroupsResponse, generic.ResponseBase])
def get_keycloak_groups(brief: Optional[bool] = False):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        groups_req = keycloak_rest_crud.get_groups(admin_access_token=admin_access_token, brief=brief)
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
        group_req = keycloak_rest_crud.get_group(admin_access_token=admin_access_token, id=id)
        if group_req.status_code == 200: return generate_response(
            "SUCCESS",
            "Group is returned",
            group_req.data
        )
        else: return generate_response(
            "FAILURE",
            "Cannot get group",
            group_req.data
        )
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))



@router.get("/{id}/members", response_model=Union[user_schema.GetUsersResponse, generic.ResponseBase])
def get_group_members(id: str):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        group_members_req = keycloak_rest_crud.get_group_members(admin_access_token=admin_access_token, id=id)
        if group_members_req.status_code == 200: return generate_response(
            "SUCCESS",
            "Group members are returned",
            group_members_req.data
        )
        else: return generate_response(
            "FAILURE",
            "Cannot get group members",
            group_members_req.data
        )
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.put("/{id}", response_model=Union[group_schema.GetGroupResponse, generic.ResponseBase])
def edit_keycloak_group(id: str, data: group_schema.EditGroupRequest):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        edit_group_req = keycloak_rest_crud.edit_group(admin_access_token=admin_access_token, id=id, data=data)
        if edit_group_req.status_code == 204: return generate_response(
            "SUCCESS",
            "Group is updated",
            edit_group_req.data
        )
        else: return generate_response(
            "FAILURE",
            "Cannot update group",
            edit_group_req.data
        )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.delete("/{id}", response_model=Union[group_schema.GetGroupResponse, generic.ResponseBase])
def delete_keycloak_group(id: str):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        delete_group_req = keycloak_rest_crud.delete_group(admin_access_token=admin_access_token, id=id)
        if delete_group_req.status_code == 204: return generate_response(
            "SUCCESS",
            "Group is deleted",
            delete_group_req.data
        )
        else: return generate_response(
            "FAILURE",
            "Cannot delete group",
            delete_group_req.data
        )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{id}/attributes", response_model=Union[group_schema.GetGroupAttributesResponse, generic.ResponseBase])
def get_group_attributes(id: str):
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        attributes_req = keycloak_rest_crud.get_group_attributes(admin_access_token=admin_access_token, id=id)
        if attributes_req.status_code == 200: return generate_response(
            "SUCCESS",
            "Group's attributes are returned",
            attributes_req.data
        )
        else: return generate_response(
            "FAILURE",
            "Cannot get group's attributes",
            attributes_req.data
        )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))