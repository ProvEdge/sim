from typing import Sequence
from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel

from .routes import app_controller
from app.functions.general_functions import authorize, match_identity
from database.schemas import keycloak_schema

router = APIRouter()

router.include_router(
    app_controller.router,
    prefix="/sim",
    dependencies=[Depends(authorize)]
    #responses={418: {"description": "I'm a teapot"}},
)

@router.get("")
async def v0_root(credentials: keycloak_schema.Credentials = Depends(authorize)):
    return {
        "status": "SUCCES",
        "message": "API V0 Root",
        "data": credentials.dict()
    }

@router.get("/get-kubeapps-token")
async def v0_identity(identity: keycloak_schema.Identity = Depends(match_identity)):
    return {
        "status": "SUCCES",
        "message": "API V0 Root",
        "data": identity.dict()
    }