from typing import List, Optional, Union
from pydantic import BaseModel
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.sqltypes import NullType

from .generic import ResponseBase

class RobotBase(BaseModel):
    type: str
    has_gpu: bool
    gpu_mb: int
    cpu_mb: int
    ram_mb: int
    helm_values: str

class RobotCreate(RobotBase):
    pass

class RobotEdit(BaseModel):
    type: Optional[str]
    has_gpu: Optional[bool]
    gpu_mb: Optional[int]
    cpu_mb: Optional[int]
    ram_mb: Optional[int]
    helm_values: Optional[str]

class Robot(RobotBase):
    class Config:
        orm_mode = True

class ListRobotsResponse(ResponseBase):
    data: List[Robot]

class GetRobotResponse(ResponseBase):
    data: Robot