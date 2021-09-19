from fastapi import APIRouter

from .routes import app_controller

router = APIRouter()

router.include_router(
    app_controller.router,
    prefix="/sim",
    #responses={418: {"description": "I'm a teapot"}},
)

@router.get("")
async def v0_root():
    return {
        "status": "SUCCES",
        "message": "API V0 Root"
    }