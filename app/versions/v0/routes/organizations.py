from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Union

from app import models
from database.schemas import generic, organization_schema
from database.database import engine

from app.functions import organization_crud, keycloak_auth, keycloak_rest_crud
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("", response_model=Union[dict, generic.ResponseBase])
def get_keycloak_groups():
    try:
        admin_access_token = keycloak_auth.get_admin_credentials()["access_token"]
        groups = keycloak_rest_crud.get_groups(admin_access_token=admin_access_token)
        return groups
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))