from fastapi import APIRouter

from . import organizations

router = APIRouter()

router.include_router(
    organizations.router,
    prefix="/organizations",
    tags=["Organizations"]
    #responses={418: {"description": "I'm a teapot"}},
)

