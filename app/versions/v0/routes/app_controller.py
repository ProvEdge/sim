from fastapi import APIRouter
from sqlalchemy.sql.expression import desc

from typing import Union
from database.schemas import generic, keycloak_schema
from app.functions import general_functions, keycloak_auth

from . import organizations, users

router = APIRouter()

router.include_router(
    organizations.router,
    prefix="/organizations",
    tags=["Organizations"]
    #responses={418: {"description": "I'm a teapot"}},
)

router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
    #responses={418: {"description": "I'm a teapot"}},
)

@router.get("/get-keycloak-admin-credentials", response_model=Union[keycloak_schema.AdminAccessCredentials, generic.ResponseBase])
def get_keycloak_admin_credentials():
    try:
        creds = keycloak_auth.get_admin_credentials()
        return creds
    except Exception as e:
        return general_functions.generate_response(status="FAILURE", message=str(e))

