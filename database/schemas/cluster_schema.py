from typing import List, Optional
from fastapi_camelcase import CamelModel

from .generic import ResponseBase

class ClusterBase(CamelModel):
    api_server_address: str
    group_id: str

class ClusterCreate(ClusterBase):
    pass

class ClusterEdit(CamelModel):
    api_server_address: Optional[str]
    group_id: Optional[str]

class Cluster(ClusterBase):
    id: int
    class Config:
        orm_mode = True

class ListClustersResponse(ResponseBase):
    data: List[Cluster]

class GetClusterResponse(ResponseBase):
    data: Cluster

