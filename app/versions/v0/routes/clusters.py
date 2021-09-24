
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Union

from app import models
from database.schemas import generic, cluster_schema
from database.database import engine

from app.functions import cluster_crud
from app.functions.general_functions import get_db, generate_response

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("", response_model=Union[cluster_schema.ListClustersResponse, generic.ResponseBase])
def read_clusters(group_id: Optional[str] = "", api_server_address: Optional[str] = "", skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        clusters = cluster_crud.get_clusters(db, group_id=group_id, api_server_address=api_server_address, skip=skip, limit=limit)
        return generate_response("SUCCESS", "Clusters are returned", clusters)
    except Exception as e:
        return generate_response(status="FAILURE", message=str(e))


@router.get("/{id}", response_model=Union[cluster_schema.GetClusterResponse, generic.ResponseBase])
def read_cluster_by_id(id: int, db: Session = Depends(get_db)):
    try:
        db_cluster = cluster_crud.get_cluster(db, id=id)
        if db_cluster is None:
            return generate_response(
                "FAILURE",
                "Cluster not found"
            )
        return generate_response(
            "SUCCESS",
            "Cluster is returned",
            db_cluster
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

# @router.get("/name/{name}", response_model=Union[organization_schema.GetOrganizationResponse, generic.ResponseBase])
# def read_organization_by_name(name: str, db: Session = Depends(get_db)):
#     try:
#         db_org = organization_crud.get_organization_by_name(db, name=name)
#         if db_org is None:
#             return generate_response(
#                 "FAILURE",
#                 "No such an organization found"
#             )
#         return generate_response(
#             "SUCCESS",
#             "Organization is returned",
#             db_org
#         )
#     except Exception as e:
#         return generate_response(
#             "FAILURE",
#             str(e)
#         )

@router.post("", response_model=Union[cluster_schema.GetClusterResponse, generic.ResponseBase])
def create_cluster(cluster: cluster_schema.ClusterCreate, db: Session = Depends(get_db)):
    try:
        cls = cluster_crud.create_cluster(db=db, cluster=cluster)

        return generate_response(
            "SUCCESS",
            "Cluster is created",
            cls
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.patch("/{id}", response_model=Union[cluster_schema.GetClusterResponse, generic.ResponseBase])
def edit_cluster(cluster: cluster_schema.ClusterEdit, id: int, db: Session = Depends(get_db)):
    try:
        db_cluster = cluster_crud.get_cluster(db, id=id)

        if not db_cluster:
            return generate_response(
                "FAILURE",
                "This cluster does not exist"
            )

        cls = cluster_crud.edit_cluster(db=db, cluster=cluster, id=id)

        return generate_response(
            "SUCCESS",
            "Cluster is edited",
            cls
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )

@router.delete("/{id}", response_model=Union[cluster_schema.GetClusterResponse, generic.ResponseBase])
def delete_cluster(id: int, db: Session = Depends(get_db)):
    try:
        db_cluster = cluster_crud.get_cluster(db, id=id)
        if db_cluster is None:
            return generate_response(
                "FAILURE",
                "Cluster not found"
            )

        delete_exec = cluster_crud.delete_cluster(db, id=id)
        return generate_response(
            "SUCCESS",
            "Cluster is deleted",
            delete_exec
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )