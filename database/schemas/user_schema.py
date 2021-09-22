from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

#   User Representation
# {
#     "id": "366c1077-618d-412b-b7bb-e641649d4788",
#     "createdTimestamp": 1629549438900,
#     "username": "engin",
#     "enabled": true,
#     "totp": false,
#     "emailVerified": true,
#     "firstName": "Engin",
#     "lastName": "Gungor",
#     "email": "esgungor@etu.edu.tr",
#     "attributes": {
#         "ne-vereyim-abime": [
#         "ne-vereceksin-bana"
#         ]
#     },
#     "disableableCredentialTypes": [],
#     "requiredActions": [],
#     "notBefore": 0,
#     "access": {
#         "manageGroupMembership": true,
#         "view": true,
#         "mapRoles": true,
#         "impersonate": true,
#         "manage": true
#     }
# }

class UserRepresentation(BaseModel):
    id: str
    createdTimestamp: Optional[int]
    username: str
    totp: Optional[bool]
    emailVerified: Optional[bool]
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    attributes: Optional[dict]
    disableableCredentialTypes: Optional[List[str]]
    requiredActions: Optional[List[str]]
    notBefore: Optional[int]
    access: Optional[dict]

class GetUserResponse(ResponseBase):
    data: UserRepresentation

class GetUsersResponse(ResponseBase):
    data: List[UserRepresentation]

class EditUserRequest(BaseModel):
    email: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]

class GetUserAttributesResponse(ResponseBase):
    data: dict