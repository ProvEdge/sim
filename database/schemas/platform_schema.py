from typing import List
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

# "data": [
#     {
#         "releaseName": "my-jacky",
#         "version": "0.1.3",
#         "namespace": "tunahan",
#         "status": "deployed",
#         "chart": "jackal",
#         "chartMetadata": {
#             "name": "jackal",
#             "version": "0.1.3",
#             "description": "Jackal Helm Chart",
#             "apiVersion": "v2",
#             "appVersion": "1.16.0",
#             "type": "application"
#         }
#     }
# ]

class Release(CamelModel):
    release_name: str
    version: str
    namespace: str
    status: str
    chart: str

class ListReleasesResponseData(CamelModel):
    data: List[Release]

class ListReleasesResponse(ResponseBase):
    data: ListReleasesResponseData
