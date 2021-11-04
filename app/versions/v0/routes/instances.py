
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Union

from app import models
from database.schemas import generic, instance_schema, keycloak_schema
from database.database import engine

from app.functions import instance_crud
from app.functions.general_functions import get_db, generate_response, authorize

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get(
    path="", 
    response_model=Union[instance_schema.ListInstancesResponse, generic.ResponseBase],
    tags=["Platform"]
)
def read_instances(
    credentials: keycloak_schema.Credentials = Depends(authorize),
    belongs_to_group: Optional[bool] = False, 
    group_id: Optional[str] = "", 
    cluster_id: Optional[int] = 0, 
    robot_type: Optional[str] = "", 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        instances = instance_crud.get_instances(
            db=db, 
            user_id=credentials.user_id, 
            belongs_to_group=belongs_to_group, 
            group_id=group_id, 
            cluster_id=cluster_id, 
            robot_type=robot_type, 
            skip=skip, 
            limit=limit
        )
        
        return generate_response("SUCCESS", "Instances are returned", instances)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get(
    path="/{id}", 
    response_model=Union[instance_schema.GetInstanceResponse, generic.ResponseBase],
    tags=["Platform"]
)
def read_instance_by_id(
    id: int, 
    credentials: keycloak_schema.Credentials = Depends(authorize),
    db: Session = Depends(get_db)
):
    try:
        db_instance = instance_crud.get_instance(
            db, 
            id=id,
            credentials=credentials
        )
        if db_instance is None:
            return generate_response(
                "FAILURE",
                "Instance not found"
            )
        return generate_response(
            "SUCCESS",
            "Instance is returned",
            db_instance
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.post(
    path="", 
    response_model=Union[instance_schema.GetInstanceResponse, generic.ResponseBase]
)
def create_instance(
    instance: instance_schema.InstanceCreate,
    credentials: keycloak_schema.Credentials = Depends(authorize),
    db: Session = Depends(get_db)
):
    try:
        ins = instance_crud.create_instance(
            db=db, 
            instance=instance,
            credentials=credentials
        )

        return generate_response(
            "SUCCESS",
            "Instance is created",
            ins
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.patch(
    path="/{id}", 
    response_model=Union[instance_schema.GetInstanceResponse, generic.ResponseBase]
)
def edit_instance(
    instance: instance_schema.InstanceEdit, 
    id: int, 
    credentials: keycloak_schema.Credentials = Depends(authorize),
    db: Session = Depends(get_db)
):
    try:
        db_instance = instance_crud.get_instance(
            db=db, 
            id=id,
            credentials=credentials
        )

        if not db_instance:
            return generate_response(
                "FAILURE",
                "This instance does not exist"
            )

        ins = instance_crud.edit_instance(
            db=db, 
            instance=instance, 
            id=id,
            credentials=credentials
        )

        return generate_response(
            "SUCCESS",
            "Instance is edited",
            ins
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.delete(
    path="/{id}", response_model=Union[instance_schema.GetInstanceResponse, generic.ResponseBase]
)
def delete_instance(
    id: int, 
    db: Session = Depends(get_db),
    credentials: keycloak_schema.Credentials = Depends(authorize)
):
    try:
        db_instance = instance_crud.get_instance(
            db, 
            id=id,
            credentials=credentials
        )
        if db_instance is None:
            return generate_response(
                "FAILURE",
                "Instance not found"
            )

        delete_exec = instance_crud.delete_instance(
            db, 
            id=id,
            credentials=credentials
        )
        return generate_response(
            "SUCCESS",
            "Instance is deleted",
            delete_exec
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )