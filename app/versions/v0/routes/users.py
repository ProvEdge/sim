from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Union

from app import models
from database.schemas import generic, user_schema
from database.database import engine

from app.functions import user_crud
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("", response_model=Union[user_schema.ListUsersResponse, generic.ResponseBase])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        users = user_crud.get_users(db, skip=skip, limit=limit)
        return generate_response("SUCCESS", "Users are returned", users)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{id}", response_model=Union[user_schema.GetUserResponse, generic.ResponseBase])
def read_user_by_id(id: int, db: Session = Depends(get_db)):
    try:
        db_user = user_crud.get_user(db, id=id)
        if db_user is None:
            return generate_response(
                "FAILURE",
                "No such a user found"
            )
        return generate_response(
            "SUCCESS",
            "User is returned",
            db_user
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.get("/name/{name}", response_model=Union[user_schema.GetUserResponse, generic.ResponseBase])
def read_user_by_name(name: str, db: Session = Depends(get_db)):
    try:
        db_user = user_crud.get_user_by_name(db, name=name)
        if db_user is None:
            return generate_response(
                "FAILURE",
                "No such a user found"
            )
        return generate_response(
            "SUCCESS",
            "User is returned",
            db_user
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.post("", response_model=Union[user_schema.GetUserResponse, generic.ResponseBase])
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = user_crud.get_user_by_email(db, email=user.email)

        if db_user:
            return generate_response(
                "FAILURE",
                "This user exists"
            )
        
        new_user = user_crud.create_user(db=db, user=user)

        return generate_response(
            "SUCCESS",
            "User is created",
            new_user
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.patch("/{id}", response_model=Union[user_schema.GetUserResponse, generic.ResponseBase])
def edit_user(user: dict, id: int, db: Session = Depends(get_db)):
    try:
        db_user = user_crud.get_user(db, id=id)

        if not db_user:
            return generate_response(
                "FAILURE",
                "This user does not exist"
            )
        
        edit_user = user_crud.edit_user(db=db, user=user, id=id)

        return generate_response(
            "SUCCESS",
            "User is edited",
            edit_user
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.delete("/{id}", response_model=Union[user_schema.GetUserResponse, generic.ResponseBase])
def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        db_user = user_crud.get_user(db, id=id)
        if db_user is None:
            return generate_response(
                "FAILURE",
                "No such a user found"
            )

        user_crud.delete_user(db, id=id)
        return generate_response(
            "SUCCESS",
            "User is deleted",
            db_user
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )