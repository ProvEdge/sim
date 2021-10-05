from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase
from database.schemas import git_schema, argocd_schema

class K8sResponse():
    def __init__(self, status_code: int, data: dict):
        self.status_code = status_code
        self.data = data

class CreateInstance(BaseModel):
    argocd_app: argocd_schema.CreateApplicationRequest
    gitops: git_schema.AddValuesToGit


# class ClusterBase(BaseModel):
#     api_server_address: str
#     group_id: str

# class ClusterCreate(ClusterBase):
#     pass

# class ClusterEdit(BaseModel):
#     api_server_address: Optional[str]
#     group_id: Optional[str]

# class Cluster(ClusterBase):
#     id: int
#     class Config:
#         orm_mode = True

# class ListClustersResponse(ResponseBase):
#     data: List[Cluster]

# class GetClusterResponse(ResponseBase):
#     data: Cluster

