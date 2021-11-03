from fastapi_camelcase import CamelModel
from database.schemas.generic import ResponseBase

class PlatformResponse(CamelModel):
    status_code: int
    message: str
    data: dict

class CreateInstance(CamelModel):
    name: str
    robot_type: str

class CreateInstanceResponse(ResponseBase):
    data: dict

# class ListInstancesServiceResponse(CamelModel):
#     release_name