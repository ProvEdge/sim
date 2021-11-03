from typing import List, Optional
from fastapi_camelcase import CamelModel

from .generic import ResponseBase

class InstanceBase(CamelModel):
    name: str
    user_id: str
    # belongs_to_group: bool
    # group_id: str
    # cluster_id: int
    namespace: str = "tunahan"
    robot_type: str = "jackal"
    release_name: str
    helm_values: str = ""

class InstanceCreate(CamelModel):
    name: str
    # user_id: str
    # belongs_to_group: bool
    # group_id: str
    # cluster_id: int
    namespace: str = "tunahan"
    robot_type: str = "jackal"
    release_name: str
    helm_values: str = ""

class InstanceEdit(CamelModel):
    name: Optional[str]
    # user_id: Optional[str]
    # belongs_to_group: Optional[bool]
    # group_id: Optional[str]
    # cluster_id: Optional[int]
    namespace: Optional[str]
    robot_type: Optional[str]
    release_name: Optional[str]
    helm_values: Optional[str]

class Instance(InstanceBase):
    id: int
    class Config:
        orm_mode = True

class ListInstancesResponse(ResponseBase):
    data: List[Instance]

class GetInstanceResponse(ResponseBase):
    data: Instance

