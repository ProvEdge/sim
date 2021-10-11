
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

@router.get("/{owner}/{repo}")
def get_repo(owner: str, repo: str, url: str = "https://gitea.provedge.cloud/api/v1", access_token: str = "194e5b33eef95a4f905b4c28ede9bf8f76173b11"):
    try:
        repo = gitea_rest_crud.get_repository(
            url=url,
            access_token=access_token,
            owner=owner,
            repo=repo
        )
        
        return generate_response("SUCCESS", "Clusters are returned", repo)
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


@router.get("/file-content/{owner}/{repo}/{filepath}")
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


@router.post("/file-content/{owner}/{repo}/{filepath}")
def get_file_content(
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


# @router.get("/{id}", response_model=Union[cluster_schema.GetClusterResponse, generic.ResponseBase])
# def read_cluster_by_id(id: int, db: Session = Depends(get_db)):
#     try:
#         db_cluster = cluster_crud.get_cluster(db, id=id)
#         if db_cluster is None:
#             return generate_response(
#                 "FAILURE",
#                 "Cluster not found"
#             )
#         return generate_response(
#             "SUCCESS",
#             "Cluster is returned",
#             db_cluster
#         )
#     except Exception as e:
#         return generate_response(
#             "FAILURE",
#             str(e)
#         )

# # @router.get("/name/{name}", response_model=Union[organization_schema.GetOrganizationResponse, generic.ResponseBase])
# # def read_organization_by_name(name: str, db: Session = Depends(get_db)):
# #     try:
# #         db_org = organization_crud.get_organization_by_name(db, name=name)
# #         if db_org is None:
# #             return generate_response(
# #                 "FAILURE",
# #                 "No such an organization found"
# #             )
# #         return generate_response(
# #             "SUCCESS",
# #             "Organization is returned",
# #             db_org
# #         )
# #     except Exception as e:
# #         return generate_response(
# #             "FAILURE",
# #             str(e)
# #         )

# @router.post("", response_model=Union[cluster_schema.GetClusterResponse, generic.ResponseBase])
# def create_cluster(cluster: cluster_schema.ClusterCreate, db: Session = Depends(get_db)):
#     try:
#         cls = cluster_crud.create_cluster(db=db, cluster=cluster)

#         return generate_response(
#             "SUCCESS",
#             "Cluster is created",
#             cls
#         )
#     except Exception as e:
#         return generate_response(
#             "FAILURE",
#             str(e)
#         )


# @router.patch("/{id}", response_model=Union[cluster_schema.GetClusterResponse, generic.ResponseBase])
# def edit_cluster(cluster: cluster_schema.ClusterEdit, id: int, db: Session = Depends(get_db)):
#     try:
#         db_cluster = cluster_crud.get_cluster(db, id=id)

#         if not db_cluster:
#             return generate_response(
#                 "FAILURE",
#                 "This cluster does not exist"
#             )

#         cls = cluster_crud.edit_cluster(db=db, cluster=cluster, id=id)

#         return generate_response(
#             "SUCCESS",
#             "Cluster is edited",
#             cls
#         )
#     except Exception as e:
#         return generate_response(
#             "FAILURE",
#             str(e)
#         )

# @router.delete("/{id}", response_model=Union[cluster_schema.GetClusterResponse, generic.ResponseBase])
# def delete_cluster(id: int, db: Session = Depends(get_db)):
#     try:
#         db_cluster = cluster_crud.get_cluster(db, id=id)
#         if db_cluster is None:
#             return generate_response(
#                 "FAILURE",
#                 "Cluster not found"
#             )

#         delete_exec = cluster_crud.delete_cluster(db, id=id)
#         return generate_response(
#             "SUCCESS",
#             "Cluster is deleted",
#             delete_exec
#         )
#     except Exception as e:
#         return generate_response(
#             "FAILURE",
#             str(e)
#         )