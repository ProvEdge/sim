
from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session

from app.functions.general_functions import generate_response, get_db, match_identity
from app.functions.prefect_tasks import create_instance
from database.schemas import keycloak_schema, platform_schema


router = APIRouter()

@router.get("/create")
def create_flow():
    try:
        create_instance.create_flow()
    
        return generate_response("SUCCESS", "Workflow is created", {})
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.post("/run")
def run_flow(
    instance: platform_schema.CreateInstance,
    identity: keycloak_schema.Identity = Depends(match_identity),
):
    try:
        import prefect
        from prefect.client.client import Client

        cli = Client()

        cli.create_flow_run(
            version_group_id="7a9a7ef9-1e2f-47f1-a5a0-6fa7d2160038",
            run_name="runy",
            parameters=dict(
                identity=identity.dict(),
                name=instance.name,
                robot_type=instance.robot_type
            )
        )
    
        return generate_response("SUCCESS", "Workflow is created", {})
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


