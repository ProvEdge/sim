from fastapi import APIRouter
from sqlalchemy.sql.expression import desc

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
