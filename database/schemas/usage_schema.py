from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

class UsageBase(BaseModel):
    start_time: datetime
    end_time: datetime
    is_terminated: bool

    ins_id: int
    ins_name: str
    ins_user_id: str
    ins_belongs_to_group: bool
    ins_group_id: str
    ins_cluster_id: int
    # storage_id
    ins_namespace: str
    ins_deployment: str
    ins_robot_type: str


class UsageCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    instance_id: int

class UsageEdit(BaseModel):
    pass

class Usage(UsageBase):
    id: int
    class Config:
        orm_mode = True

class ListUsageResponse(ResponseBase):
    data: List[Usage]

class GetUsageResponse(ResponseBase):
    data: Usage

