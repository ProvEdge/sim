from typing import List
from pydantic import BaseModel

from .generic import ResponseBase

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int

    class Config:
        orm_mode = True

class ListOrganizationsResponse(ResponseBase):
    data: List[Organization]

class GetOrganizationResponse(ResponseBase):
    data: Organization