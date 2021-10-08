from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel
from sqlalchemy.sql.elements import Null

from .generic import ResponseBase

class UsageBase(BaseModel):
    start_time: datetime
    end_time: Optional[datetime]
    is_terminated: bool

    ins_id: int
    ins_name: str
    ins_user_id: str
    ins_belongs_to_group: bool
    ins_group_id: str
    ins_cluster_id: int
    # storage_id
    ins_namespace: str
    #ins_deployment: str
    #ins_service: str
    #ins_configmaps: str
    ins_robot_type: str
    ins_values_repository: str
    ins_values_path: str
    ins_argocd_project_name: str

class UsageCreate(BaseModel):
    instance_id: int

class UsageEdit(BaseModel):
    end_time: Optional[datetime]
    is_terminated: Optional[bool]

class Usage(UsageBase):
    id: int
    class Config:
        orm_mode = True

class ListUsageResponse(ResponseBase):
    data: List[Usage]

class GetUsageResponse(ResponseBase):
    data: Usage

