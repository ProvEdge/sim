from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

class InstanceBase(BaseModel):
    name: str
    user_id: str
    belongs_to_group: bool
    group_id: str
    cluster_id: int
    namespace: str
    deployment: str
    robot_type: str

class InstanceCreate(InstanceBase):
    pass

class InstanceEdit(BaseModel):
    name: Optional[str]
    user_id: Optional[str]
    belongs_to_group: Optional[bool]
    group_id: Optional[str]
    cluster_id: Optional[int]
    namespace: Optional[str]
    deployment: Optional[str]
    robot_type: Optional[str]

class Instance(InstanceBase):
    id: int
    class Config:
        orm_mode = True

class ListInstancesResponse(ResponseBase):
    data: List[Instance]

class GetInstanceResponse(ResponseBase):
    data: Instance

