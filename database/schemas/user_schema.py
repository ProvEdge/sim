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

# class UserRepresentation(BaseModel):
#     id: str
#     createdTimestamp: Optional[int]
#     username: str
#     totp: 
#     emailVerified: 
#     firstName: 
#     lastName: 
#     email: 
#     attributes: 
#     disableableCredentialTypes: 