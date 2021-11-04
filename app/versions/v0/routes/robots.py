
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Union

from app import models
from database.schemas import generic, robot_schema
from database.database import engine

from app.functions import robot_crud
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get(
    path="", 
    response_model=Union[robot_schema.ListRobotsResponse, generic.ResponseBase],
    tags=["Platform"]
)
def read_robots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        robots = robot_crud.get_robots(db, skip=skip, limit=limit)
        return generate_response("SUCCESS", "Robots are returned", robots)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get(
    path="/{type}", 
    response_model=Union[robot_schema.GetRobotResponse, generic.ResponseBase],
    tags=["Platform"]
)
def read_robot_by_type(type: str, db: Session = Depends(get_db)):
    try:
        db_robot = robot_crud.get_robot(db, type=type)
        if db_robot is None:
            return generate_response(
                "FAILURE",
                "Robot not found"
            )
        return generate_response(
            "SUCCESS",
            "Robot is returned",
            db_robot
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.post(
    path="", 
    response_model=Union[robot_schema.GetRobotResponse, generic.ResponseBase]
)
def create_robot(robot: robot_schema.RobotCreate, db: Session = Depends(get_db)):
    try:
        rbt = robot_crud.create_robot(db=db, robot=robot)

        return generate_response(
            "SUCCESS",
            "Robot is created",
            rbt
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.patch(
    path="/{type}", 
    response_model=Union[robot_schema.GetRobotResponse, generic.ResponseBase]
)
def edit_robot(robot: robot_schema.RobotEdit, type: str, db: Session = Depends(get_db)):
    try:
        db_robot = robot_crud.get_robot(db, type=type)

        if not db_robot:
            return generate_response(
                "FAILURE",
                "This robot does not exist"
            )

        rbt = robot_crud.edit_robot(db=db, robot=robot, type=type)

        return generate_response(
            "SUCCESS",
            "Robot is edited",
            rbt
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.delete(
    path="/{type}", 
    response_model=Union[robot_schema.GetRobotResponse, generic.ResponseBase]
)
def delete_robot(type: str, db: Session = Depends(get_db)):
    try:
        db_robot = robot_crud.get_robot(db, type=type)
        if db_robot is None:
            return generate_response(
                "FAILURE",
                "Robot not found"
            )

        delete_exec = robot_crud.delete_robot(db, type=type)
        return generate_response(
            "SUCCESS",
            "Robot is deleted",
            delete_exec
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )