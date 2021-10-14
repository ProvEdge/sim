
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


@router.get("/user")
def get_auth_user(
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):

    try:
        get_user_req = gitea_rest_crud.get_authenticated_user(
            base_url=base_url,
            access_token=access_token
        )

        if get_user_req.status_code == 200:
            return generate_response(
                "SUCCESS",
                "Authenticated user is returned",
                get_user_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot get user",
                get_user_req.data
            )

    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


# @router.post("/users", deprecated=True)
# def create_user(
#     user: gitea_schema.CreateUser,
#     base_url: str = Header(gitea_schema.base_url), 
#     admin_access_token: str = Header(gitea_schema.admin_access_token)
# ):

#     try:
#         new_user = gitea_rest_crud.create_user(
#             user=user,
#             base_url=base_url,
#             admin_access_token=admin_access_token
#         )

#         return generate_response(
#             "SUCCESS",
#             "User is created",
#             new_user
#         )
#     except Exception as e:
#         return generate_response(status="FAILURE", message=str(e))




@router.get("/{owner}/{repo}")
def get_repo(
    owner: str, 
    repo: str,
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):
    try:
        get_repo_req = gitea_rest_crud.get_repository(
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo
        )

        if get_repo_req.status_code == 200:
            return generate_response(
                "SUCCESS", 
                "Repository is returned", 
                get_repo_req.data
            )
        else: return generate_response(
            "FAILURE",
            "Cannot get repo",
            get_repo_req.data
        )

    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.post("/{owner}/{repo}/fork")
def fork_repo(
    owner: str, 
    repo: str, 
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):
    try:
        fork_repo_req = gitea_rest_crud.fork_repository(
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo
        )

        if fork_repo_req.status_code == 200:
            return generate_response(
                "SUCCESS", 
                "Repository is forked", 
                fork_repo_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot fork repo",
                fork_repo_req.data
            )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{owner}/{repo}/branches")
def get_branches(
    owner: str, 
    repo: str, 
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):
    try:
        get_branches_req = gitea_rest_crud.get_branches(
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo
        )

        if get_branches_req.status_code == 200:
            return generate_response(
                "SUCCESS", 
                "Branches are listed", 
                get_branches_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot get branches of repo",
                get_branches_req.data
            )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.post("/{owner}/{repo}/branches")
def create_branch(
    body: gitea_schema.CreateBranch,
    owner: str, 
    repo: str, 
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):
    try:
        create_branches_req = gitea_rest_crud.create_branch(
            body=body,
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo
        )

        if create_branches_req.status_code == 201:
            return generate_response(
                "SUCCESS", 
                "Branch is created", 
                create_branches_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot create branch",
                create_branches_req.data
            )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.delete("/{owner}/{repo}/branches/{branch}")
def delete_branch(
    owner: str, 
    repo: str,
    branch: str,
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):
    try:
        delete_branch_req = gitea_rest_crud.delete_branch(
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo,
            branch=branch
        )

        if delete_branch_req.status_code == 204:
            return generate_response(
                "SUCCESS", 
                "Branch is deleted", 
                delete_branch_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot delete branch",
                delete_branch_req.data
            )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{owner}/{repo}/contents/{filepath}")
def get_content(
    owner: str, 
    repo: str,
    filepath: str,
    branch: str = "",
    base_url: str = Header(gitea_schema.base_url), 
    access_token: str = Header(gitea_schema.access_token)
):
    try:
        get_content_req = gitea_rest_crud.get_file_content(
            base_url=base_url,
            access_token=access_token,
            owner=owner,
            repo=repo,
            branch=branch,
            filepath=filepath
        )

        if get_content_req.status_code == 200:
            return generate_response(
                "SUCCESS", 
                "Contents are returned", 
                get_content_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot get content",
                get_content_req.data
            )
        
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))

# @router.put("/rename/{owner}/{repo}")
# def rename_repo(
#     name: gitea_schema.RenameRepo, 
#     owner: str, 
#     repo: str, 
#     base_url: str = Header(gitea_schema.base_url), 
#     access_token: str = Header(gitea_schema.access_token)
# ):
#     try:
#         repo = gitea_rest_crud.change_repo_name(
#             base_url=base_url,
#             access_token=access_token,
#             owner=owner,
#             repo=repo,
#             new_name=name.new_name
#         )
        
#         return generate_response("SUCCESS", "Repository is renamed", repo)
#     except Exception as e:
#         return generate_response(status="FAILURE", message=str(e))


# @router.delete("/{owner}/{repo}")
# def delete_repo(
#     owner: str, 
#     repo: str, 
#     base_url: str = Header(gitea_schema.base_url), 
#     access_token: str = Header(gitea_schema.access_token)
# ):
#     try:
#         repo = gitea_rest_crud.delete_repository(
#             base_url=base_url,
#             access_token=access_token,
#             owner=owner,
#             repo=repo
#         )
        
#         return generate_response("SUCCESS", "Repository is deleted", repo)
#     except Exception as e:
#         return generate_response(status="FAILURE", message=str(e))


# @router.post("/repository")
# def create_repo(
#     data: gitea_schema.CreateRepository, 
#     base_url: str = Header(gitea_schema.base_url), 
#     access_token: str = Header(gitea_schema.access_token)
# ):

#     try:
#         new_repo_request = gitea_rest_crud.create_repository(
#             base_url=base_url,
#             access_token=access_token,
#             data=data
#         )

#         if new_repo_request.is_successful:
#             return generate_response(
#                 "SUCCESS",
#                 "Repository is created",
#                 new_repo_request.data
#             )
#         else: return generate_response(
#             "FAILURE",
#             "Error when creating new repository",
#             new_repo_request.data
#         )
#     except Exception as e:
#         return generate_response(
#             "FAILURE",
#             "Cannot create repository, " + str(e)
#         )


# @router.get("/file-content/{owner}/{repo}")
# def get_file_content(
#     owner: str,
#     repo: str,
#     filepath: str,
#     base_url: str = Header(gitea_schema.base_url), 
#     access_token: str = Header(gitea_schema.access_token)
# ):

#     try:
#         get_content_request = gitea_rest_crud.get_file_content(
#             base_url=base_url,
#             access_token=access_token,
#             owner=owner,
#             repo=repo,
#             filepath=filepath
#         )
#         if get_content_request.is_successful:
#             return generate_response(
#                 "SUCCESS",
#                 "File content is fetched",
#                 get_content_request.data
#             )
#         else: return generate_response(
#             "FAILURE",
#             "Error when fetching file content",
#             get_content_request.data
#         )
#     except Exception as e:
#         return generate_response(
#             "FAILURE",
#             "Cannot get file contents, " + str(e)
#         )


# @router.post("/file-content/{owner}/{repo}")
# def create_file(
#     body: gitea_schema.CreateFile,
#     owner: str,
#     repo: str,
#     filepath: str,
#     base_url: str = Header(gitea_schema.base_url), 
#     access_token: str = Header(gitea_schema.access_token)
# ):

#     try:
#         create_file_request = gitea_rest_crud.create_file(
#             data=body,
#             base_url=base_url,
#             access_token=access_token,
#             owner=owner,
#             repo=repo,
#             filepath=filepath
#         )
#         if create_file_request.is_successful:
#             return generate_response(
#                 "SUCCESS",
#                 "File created",
#                 create_file_request.data
#             )
#         else: return generate_response(
#             "FAILURE",
#             "Error when creating file",
#             create_file_request.data
#         )
#     except Exception as e:
#         return generate_response(
#             "FAILURE",
#             "Cannot create file, " + str(e)
#         )

# @router.put("/file-content/{owner}/{repo}")
# def update_file(
#     body: gitea_schema.UpdateFile,
#     owner: str,
#     repo: str,
#     filepath: str,
#     base_url: str = Header(gitea_schema.base_url), 
#     access_token: str = Header(gitea_schema.access_token)
# ):

#     try:
#         update_file_request = gitea_rest_crud.update_file(
#             data=body,
#             base_url=base_url,
#             access_token=access_token,
#             owner=owner,
#             repo=repo,
#             filepath=filepath
#         )
#         if update_file_request.is_successful:
#             return generate_response(
#                 "SUCCESS",
#                 "File updated",
#                 update_file_request.data
#             )
#         else: return generate_response(
#             "FAILURE",
#             "Error when updating file",
#             update_file_request.data
#         )
#     except Exception as e:
#         return generate_response(
#             "FAILURE",
#             "Cannot create file, " + str(e)
#         )


