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



@router.delete(
    path="/delete/{id}",
    description="Delete instance."
)
def delete_instance(
    id: int,
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token),
    db: Session = Depends(get_db)
):
    try:

        delete_req = instance_management.delete_instance(
            base_url=base_url,
            access_token=access_token,
            instance_id=id,
            db=db
        )

        if delete_req.status_code == 200:
            return generate_response(
                "SUCCESS",
                "Instance is deleted",
                delete_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot delete instance",
                delete_req.data
            )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )



@router.get(
    path="/refresh/{id}",
    description="Refresh instance, pull again from Gitea."
)
def refresh_instance(
    id: int,
    db: Session = Depends(get_db)
):
    try:

        refresh_req = instance_management.refresh_instance(
            instance_id=id,
            db=db
        )

        if refresh_req.status_code == 200:
            return generate_response(
                "SUCCESS",
                "Instance is refreshed",
                refresh_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot refresh instance",
                refresh_req.data
            )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )



@router.get(
    path="/start/{id}",
    description="Starts instance, increases replicas from 0 to 1."
)
def start_instance(
    id: int,
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token),
    db: Session = Depends(get_db)
):
    try:

        start_instance_req = instance_management.start_instance(
            base_url=base_url,
            access_token=access_token,
            instance_id=id,
            db=db
        )

        if start_instance_req.status_code == 200:
            return generate_response(
                "SUCCESS",
                "Instance is started",
                start_instance_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot",
                start_instance_req.data
            )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )



@router.get(
    path="/stop/{id}",
    description="Stops instance, decreases replicas from 1 to 0."
)
def stop_instance(
    id: int,
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token),
    db: Session = Depends(get_db)
):
    try:

        stop_instance_req = instance_management.stop_instance(
            base_url=base_url,
            access_token=access_token,
            instance_id=id,
            db=db
        )

        if stop_instance_req.status_code == 200:
            return generate_response(
                "SUCCESS",
                "Instance is stopped",
                stop_instance_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot",
                stop_instance_req.data
            )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )
