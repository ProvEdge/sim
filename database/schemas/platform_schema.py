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


# {
#   "status": "string",
#   "message": "string",
#   "data": {
#     "creationStatus": {
#       "instance": {
#         "success": true,
#         "message": "string"
#       },
#       "kubeapps": {
#         "success": true,
#         "message": "string"
#       },
#       "minio": {
#         "success": true,
#         "message": "string"
#       }
#     }
#   }
# }

class CreateReleaseInstanceStatus(CamelModel):
    success: bool
    message: str

class CreateReleaseKubeappsStatus(CreateReleaseInstanceStatus):
    pass

class CreateReleaseMinioStatus(CreateReleaseInstanceStatus):
    pass

class CreateReleaseStatus(CamelModel):
    instance: CreateReleaseInstanceStatus
    kubeapps: CreateReleaseKubeappsStatus
    minio: CreateReleaseMinioStatus

class CreateReleaseResponseData(CamelModel):
    creation_status: CreateReleaseStatus

class CreateReleaseResponse(ResponseBase):
    data: CreateReleaseResponseData


# {
#   "status": "SUCCESS",
#   "message": "Instance is being deleted",
#   "data": {
#     "deletionStatus": {
#       "instance": {
#         "success": true,
#         "message": "Instance is deleted."
#       },
#       "kubeapps": {
#         "success": true,
#         "message": "Kubeapps release is deleted."
#       }
#     }
#   }
# }

class DeleteReleaseInstanceStatus(CamelModel):
    success: bool
    message: str

class DeleteReleaseKubeappsStatus(DeleteReleaseInstanceStatus):
    pass

class DeleteReleaseStatus(CamelModel):
    instance: DeleteReleaseInstanceStatus
    kubeapps: DeleteReleaseKubeappsStatus

class DeleteReleaseResponseData(CamelModel):
    deletion_status: DeleteReleaseStatus

class DeleteReleaseResponse(ResponseBase):
    data: DeleteReleaseResponseData

#
#


class UpdateReleaseInstanceStatus(CamelModel):
    success: bool
    message: str

class UpdateReleaseKubeappsStatus(UpdateReleaseInstanceStatus):
    pass

class UpdateReleaseMinioStatus(UpdateReleaseInstanceStatus):
    pass

class UpdateReleaseStatus(CamelModel):
    instance: UpdateReleaseInstanceStatus
    kubeapps: UpdateReleaseKubeappsStatus
    minio: UpdateReleaseMinioStatus

class UpdateReleaseResponseData(CamelModel):
    update_status: UpdateReleaseStatus

class UpdateReleaseResponse(ResponseBase):
    data: UpdateReleaseResponseData