from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Union

from app import models
from database.schemas import generic, usage_schema, keycloak_schema
from database.database import engine

from app.functions import instance_crud, usage_crud
from app.functions.general_functions import get_db, generate_response, authorize

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get(
    path="", 
    response_model=Union[usage_schema.ListUsageResponse, generic.ResponseBase],
    tags=["Platform"]
)
def read_usages(
    start_time: Optional[datetime] = "", 
    end_time: Optional[datetime] = "", 
    is_terminated: Optional[bool] = True, 
    #ins_user_id: Optional[str] = "", 
    #ins_belongs_to_group: Optional[bool] = False, 
    #ins_group_id: Optional[str] = "", 
    #ins_cluster_id: Optional[int] = 0, 
    ins_robot_type: Optional[str] = "",
    ins_id: int = 0, 
    skip: int = 0, 
    limit: int = 100, 
    credentials: keycloak_schema.Credentials = Depends(authorize),
    db: Session = Depends(get_db)
):
    try:
        usages = usage_crud.get_usages(
            db=db, 
            skip=skip, 
            limit=limit,
            start_time=start_time,
            end_time=end_time,
            is_terminated=is_terminated,
        #    ins_user_id=ins_user_id,
        #    ins_belongs_to_group=ins_belongs_to_group,
        #    ins_group_id=ins_group_id,
        #    ins_cluster_id=ins_cluster_id,
            ins_robot_type=ins_robot_type,
            ins_id=ins_id,
            credentials=credentials
        )

        return generate_response("SUCCESS", "Usages are returned", usages)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get(
    path="/{id}", 
    response_model=Union[usage_schema.GetUsageResponse, generic.ResponseBase],
    tags=["Platform"]
)
def read_usage_by_id(
    id: int, 
    credentials: keycloak_schema.Credentials = Depends(authorize),
    db: Session = Depends(get_db)
):
    try:
        db_usage = usage_crud.get_usage(
            db, 
            id=id,
            credentials=credentials
        )
        if db_usage is None:
            return generate_response(
                "FAILURE",
                "Usage not found"
            )
        return generate_response(
            "SUCCESS",
            "Usage is returned",
            db_usage
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.post(
    path="", 
    response_model=Union[dict, generic.ResponseBase]
)
def create_usage(
    usage: usage_schema.UsageCreate, 
    credentials: keycloak_schema.Credentials = Depends(authorize),
    db: Session = Depends(get_db)
):
    try:

        instance = instance_crud.get_instance(
            db=db, 
            id=usage.instance_id,
            credentials=credentials
        )
        if instance is None:
            return generate_response(
                "FAILURE",
                "Instance cannot found"
            )

        usg = usage_crud.create_usage(
            db=db, 
            usage=usage,
            credentials=credentials
        )

        return generate_response(
            "SUCCESS",
            "Usage is created",
            usg
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.patch(
    path="/{id}", 
    response_model=Union[usage_schema.GetUsageResponse, generic.ResponseBase]
)
def edit_usage(
    usage: usage_schema.UsageEdit, 
    id: int, 
    credentials: keycloak_schema.Credentials = Depends(authorize),
    db: Session = Depends(get_db)
):
    try:
        db_usage = usage_crud.get_usage(
            db=db, 
            id=id,
            credentials=credentials
        )

        if not db_usage:
            return generate_response(
                "FAILURE",
                "Usage does not exist"
            )

        usg = usage_crud.edit_usage(
            db=db, 
            usage=usage, 
            id=id,
            credentials=credentials
        )

        return generate_response(
            "SUCCESS",
            "Usage is edited",
            usg
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.delete(
    path="/{id}", 
    response_model=Union[usage_schema.GetUsageResponse, generic.ResponseBase]
)
def delete_usage(
    id: int, 
    credentials: keycloak_schema.Credentials = Depends(authorize),
    db: Session = Depends(get_db)
):
    try:
        db_usage = usage_crud.get_usage(
            db, 
            id=id,
            credentials=credentials
        )

        if db_usage is None:
            return generate_response(
                "FAILURE",
                "Usage not found"
            )

        delete_exec = usage_crud.delete_usage(
            db, 
            id=id,
            credentials=credentials
        )
        return generate_response(
            "SUCCESS",
            "Usage is deleted",
            delete_exec
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )