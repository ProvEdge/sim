from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

class InstanceBase(BaseModel):
    name: str
    user_id: str
    belongs_to_group: bool
    group_id: str
    cluster_id: int
    namespace: str = "tunahan"
    #deployment: str
    #service: str
    #configmaps: str
    robot_type: str = "jackal"
    values_repository: str = "tunahanertekin/jackal-helm"
    values_branch: str
    values_path: str = "values/"
    argocd_project_name: str

class InstanceCreate(InstanceBase):
    pass

class InstanceEdit(BaseModel):
    name: Optional[str]
    user_id: Optional[str]
    belongs_to_group: Optional[bool]
    group_id: Optional[str]
    cluster_id: Optional[int]
    namespace: Optional[str]
    #deployment: Optional[str]
    #service: Optional[str]
    #configmaps: Optional[str]
    robot_type: Optional[str]
    values_repository: Optional[str]
    values_branch: Optional[str]
    values_path: Optional[str]
    argocd_project_name: Optional[str]

class Instance(InstanceBase):
    id: int
    class Config:
        orm_mode = True

class ListInstancesResponse(ResponseBase):
    data: List[Instance]

class GetInstanceResponse(ResponseBase):
    data: Instance

