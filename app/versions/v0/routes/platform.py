
from fastapi import Depends, APIRouter

from database.schemas import keycloak_schema, kubeapps_schema

from app.functions import kubeapps_rest_crud
from app.functions.general_functions import generate_response, match_identity

router = APIRouter()

@router.get("/releases")
def get_releases(
    identity: keycloak_schema.Identity = Depends(match_identity)
):
    try:
       

        return generate_response(
            "SUCCESS", 
            ""
        )

    except Exception as e:
        return generate_response(
            status="FAILURE", 
            message=str(e)
        )
