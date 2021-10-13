
from fastapi import Depends, APIRouter, HTTPException, Header
import gitea
from pydantic.main import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, Union

from app import models
from database.schemas import generic, gitea_schema
from database.database import engine

from app.functions import gitea_rest_crud
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/users")
def get_users(
    base_url: str = Header(gitea_schema.base_url), 
    admin_access_token: str = Header(gitea_schema.admin_access_token)
):

    try:
        users = gitea_rest_crud.get_users(
            base_url=base_url,
            admin_access_token=admin_access_token
        )

        return generate_response(
            "SUCCESS",
            "Users are returned",
            users
        )
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.post("/users", deprecated=True)
def create_user(
    user: gitea_schema.CreateUser,
    base_url: str = Header(gitea_schema.base_url), 
    admin_access_token: str = Header(gitea_schema.admin_access_token)
):

    try:
        new_user = gitea_rest_crud.create_user(
            user=user,
            base_url=base_url,
            admin_access_token=admin_access_token
        )

        return generate_response(
            "SUCCESS",
            "User is created",
            new_user
        )
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))




@router.get("/{owner}/{repo}")
def get_repo(
    owner: str, 
    repo: str, 
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):
    try:
        repo = gitea_rest_crud.get_repository(
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo
        )
        
        return generate_response("SUCCESS", "Repository is returned", repo)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/fork/{owner}/{repo}")
def fork_repo(
    owner: str, 
    repo: str, 
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):
    try:
        repo = gitea_rest_crud.fork_repository(
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo
        )
        
        return generate_response("SUCCESS", "Repository is forked", repo)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.put("/rename/{owner}/{repo}")
def rename_repo(
    name: gitea_schema.RenameRepo, 
    owner: str, 
    repo: str, 
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):
    try:
        repo = gitea_rest_crud.change_repo_name(
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo,
            new_name=name.new_name
        )
        
        return generate_response("SUCCESS", "Repository is renamed", repo)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.delete("/{owner}/{repo}")
def delete_repo(
    owner: str, 
    repo: str, 
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):
    try:
        repo = gitea_rest_crud.delete_repository(
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo
        )
        
        return generate_response("SUCCESS", "Repository is deleted", repo)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.post("/repository")
def create_repo(
    data: gitea_schema.CreateRepository, 
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):

    try:
        new_repo_request = gitea_rest_crud.create_repository(
            base_url=base_url,
            access_token=access_token,
            data=data
        )

        if new_repo_request.is_successful:
            return generate_response(
                "SUCCESS",
                "Repository is created",
                new_repo_request.data
            )
        else: return generate_response(
            "FAILURE",
            "Error when creating new repository",
            new_repo_request.data
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            "Cannot create repository, " + str(e)
        )


@router.get("/file-content/{owner}/{repo}")
def get_file_content(
    owner: str,
    repo: str,
    filepath: str,
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):

    try:
        get_content_request = gitea_rest_crud.get_file_content(
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo,
            filepath=filepath
        )
        if get_content_request.is_successful:
            return generate_response(
                "SUCCESS",
                "File content is fetched",
                get_content_request.data
            )
        else: return generate_response(
            "FAILURE",
            "Error when fetching file content",
            get_content_request.data
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            "Cannot get file contents, " + str(e)
        )


@router.post("/file-content/{owner}/{repo}")
def create_file(
    body: gitea_schema.CreateFile,
    owner: str,
    repo: str,
    filepath: str,
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):

    try:
        create_file_request = gitea_rest_crud.create_file(
            data=body,
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo,
            filepath=filepath
        )
        if create_file_request.is_successful:
            return generate_response(
                "SUCCESS",
                "File created",
                create_file_request.data
            )
        else: return generate_response(
            "FAILURE",
            "Error when creating file",
            create_file_request.data
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            "Cannot create file, " + str(e)
        )

@router.put("/file-content/{owner}/{repo}")
def update_file(
    body: gitea_schema.UpdateFile,
    owner: str,
    repo: str,
    filepath: str,
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):

    try:
        update_file_request = gitea_rest_crud.update_file(
            data=body,
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo,
            filepath=filepath
        )
        if update_file_request.is_successful:
            return generate_response(
                "SUCCESS",
                "File updated",
                update_file_request.data
            )
        else: return generate_response(
            "FAILURE",
            "Error when updating file",
            update_file_request.data
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            "Cannot create file, " + str(e)
        )


