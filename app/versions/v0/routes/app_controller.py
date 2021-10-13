from fastapi import APIRouter
#from sqlalchemy.sql.expression import desc

from typing import Union

from database.schemas import generic, keycloak_schema
from app.functions import general_functions, keycloak_auth

from . import platform_instances, groups, users, clusters, robots, instances, usages, bills, pricing_formulas, gitea

router = APIRouter()

router.include_router(
    gitea.router,
    prefix="/gitea",
    tags=["Gitea"]
    #responses={418: {"description": "I'm a teapot"}},
)

router.include_router(
    platform_instances.router,
    prefix="/platform/instances",
    tags=["Instances - Platform Scope"],
    deprecated=True
    #responses={418: {"description": "I'm a teapot"}},
)

router.include_router(
    pricing_formulas.router,
    prefix="/pricing-formulas",
    tags=["Pricing Formulas"]
    #responses={418: {"description": "I'm a teapot"}},
)

router.include_router(
    bills.router,
    prefix="/bills",
    tags=["Bills"]
    #responses={418: {"description": "I'm a teapot"}},
)

router.include_router(
    groups.router,
    prefix="/groups",
    tags=["Groups"]
    #responses={418: {"description": "I'm a teapot"}},
)

router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
    #responses={418: {"description": "I'm a teapot"}},
)

router.include_router(
    clusters.router,
    prefix="/clusters",
    tags=["Clusters"]
    #responses={418: {"description": "I'm a teapot"}},
)

router.include_router(
    robots.router,
    prefix="/robots",
    tags=["Robots"]
    #responses={418: {"description": "I'm a teapot"}},
)

router.include_router(
    instances.router,
    prefix="/instances",
    tags=["Instances"]
    #responses={418: {"description": "I'm a teapot"}},
)

router.include_router(
    usages.router,
    prefix="/usages",
    tags=["Usages"]
    #responses={418: {"description": "I'm a teapot"}},
)

@router.get("/get-keycloak-admin-credentials", response_model=Union[keycloak_schema.AdminAccessCredentials, generic.ResponseBase])
def get_keycloak_admin_credentials():
    try:
        creds = keycloak_auth.get_admin_credentials()
        return creds
    except Exception as e:
        return general_functions.generate_response(status="FAILURE", message=str(e))

