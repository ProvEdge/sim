from typing import Optional, Union

from fastapi import APIRouter, Header

from app import models
from database.schemas import generic, platform_schema

from app.functions import instance_crud, kubernetes_jobs
from app.functions.general_functions import generate_response

router = APIRouter()

from database.schemas import generic

@router.post("/robot-to-instance", response_model=Union[dict, generic.ResponseBase])
def robot_to_instance(instance: platform_schema.RobotToInstanceRequest, APIServer: str = Header(None), Token: str = Header(None)):
    cm = kubernetes_jobs.apply_configmaps(
        robot=instance.robot_type,
        namespace="xxx",
        APIServer=APIServer,
        Token=Token
    )
    return {"Hello": cm}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
