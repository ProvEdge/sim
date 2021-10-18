from typing import Optional, Union

from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm.session import Session

from app import models
from database.schemas import argocd_schema, generic, gitea_schema, platform_schema, git_schema

from app.functions import argocd_rest_crud, git_rest_crud, gitea_rest_crud, instance_crud, instance_management, kubernetes_jobs
from app.functions.general_functions import generate_response, get_db

from database.database import engine
from database.schemas import generic

from gitea import *

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post(
    path="/create-instance",
    description="Fork the base repo."
)
def create_instance(
    body: gitea_schema.CreateInstance, 
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token),
    db: Session = Depends(get_db)
):
    try:

        create_repo = instance_management.create_instance(
            base_url=base_url,
            access_token=access_token,
            body=body,
            db=db
        )

        if create_repo.status_code == 200:
            return generate_response(
                "SUCCESS",
                "Instance is created",
                create_repo.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot create instance",
                create_repo.data
            )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


