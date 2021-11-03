from typing import Sequence
from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel

from .routes import app_controller
from app.functions.general_functions import authorize, match_identity
from database.schemas import keycloak_schema, generic


router = APIRouter()

router.include_router(
    app_controller.router,
    prefix="/sim",
    dependencies=[Depends(authorize)],
    responses={
        401: {
            "description": "Not authorized.",
            "model": generic.AuthError
        },
        404: {
            "description": "Not found.",
            "model": generic.ResponseBase
        },
        406: {
            "description": "Not acceptable. (Cannot perform create, update and delete)",
            "model": generic.ResponseBase
        },
        500: {
            "description": "Internal Server Error.",
            "model": str
        }
    }
    #responses={418: {"description": "I'm a teapot"}},
)

@router.get("")
async def v0_root(credentials: keycloak_schema.Credentials = Depends(authorize)):
    return {
        "tuna": "meyu"
    }

@router.get("/get-kubeapps-token")
async def v0_identity(identity: keycloak_schema.Identity = Depends(match_identity)):
    return {
        "status": "SUCCES",
        "message": "API V0 Root",
        "data": identity.dict()
    }