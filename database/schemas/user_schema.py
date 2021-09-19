from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

class UserBase(BaseModel):
    git_uid: Optional[str]
    email: str
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class ListUsersResponse(ResponseBase):
    data: List[User]

class GetUserResponse(ResponseBase):
    data: User