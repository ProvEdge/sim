from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase
from database.schemas import git_schema, argocd_schema, instance_schema

class K8sResponse():
    def __init__(self, status_code: int, data: dict):
        self.status_code = status_code
        self.data = data

class CreateInstance(BaseModel):
    access_token: str = "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"
    argo_cluster: str = "https://kubernetes.default.svc"
    helm_path: str = "."
    instance: instance_schema.InstanceCreate


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

