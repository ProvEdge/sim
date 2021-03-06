from typing import Any, List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

#   Group Representation
# {
#     "id": "06a83b33-940c-47fd-8e61-6d383a601e39",
#     "name": "platform-admin",
#     "path": "/platform-admin",
#     "attributes": {},
#     "realmRoles": [],
#     "clientRoles": {},
#     "subGroups": [],
#     "access": {
#         "view": true,
#         "manage": true,
#         "manageMembership": true
#     }
# }


class GroupRepresentation(BaseModel):
    id: str
    name: str
    path: str
    attributes: Optional[dict]
    realmRoles: Optional[List[str]]
    clientRoles: Optional[dict]
    subGroups: Optional[List[dict]]
    access: Optional[dict]


class GetGroupResponse(ResponseBase):
    data: GroupRepresentation

class GetGroupsResponse(ResponseBase):
    data: List[GroupRepresentation]

class EditGroupRequest(BaseModel):
    name: Optional[str]
    access: Optional[dict]
    attributes: Optional[dict]

class GetGroupAttributesResponse(ResponseBase):
    data: dict

class AddAttributesRequest(BaseModel):
    name: str
    attributes: dict