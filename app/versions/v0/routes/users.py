from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Union

from app import models
from database.schemas import generic, user_schema, org_user_schema
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

@router.delete("/delete/{id}", response_model=Union[user_schema.GetUserResponse, generic.ResponseBase])
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

@router.post("/attend-organization", response_model=Union[org_user_schema.ParticipationResponse, generic.ResponseBase])
def add_user_to_organization(participation: org_user_schema.OrgUser, db: Session = Depends(get_db)):
    try:
        db_org_user = user_crud.is_member(db, participation=participation)

        if db_org_user:
            return generate_response(
                "FAILURE",
                "User is already a member of this organization"
            )
        
        new_participation = user_crud.join_organization(db=db, participation=participation)

        return generate_response(
            "SUCCESS",
            "User is attended to organization",
            new_participation
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.get("/organizations/{id}", response_model=Union[org_user_schema.ListParticipations, generic.ResponseBase])
def read_users_organizations(id: int, db: Session = Depends(get_db)):
    try:
        db_user = user_crud.get_user(db, id=id)
        if db_user is None:
            return generate_response(
                "FAILURE",
                "No such a user found"
            )
        
        orgs = user_crud.get_users_organizations(db, id)
        return generate_response(
            "SUCCESS",
            "User's organizations are returned",
            orgs
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.delete("/leave-organization", response_model=Union[org_user_schema.ParticipationResponse, generic.ResponseBase])
def remove_user_from_organization(participation: org_user_schema.OrgUser, db: Session = Depends(get_db)):
    try:
        db_org_user = user_crud.is_member(db, participation=participation)
        if db_org_user is None:
            return generate_response(
                "FAILURE",
                "User is already not a member of this organization"
            )

        user_crud.leave_organization(db, participation=participation)
        return generate_response(
            "SUCCESS",
            "User is removed from organization",
            db_org_user
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )