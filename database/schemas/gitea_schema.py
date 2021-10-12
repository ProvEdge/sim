from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

base_url = "https://gitea.provedge.cloud/api/v1"
access_token = "194e5b33eef95a4f905b4c28ede9bf8f76173b11"
admin_access_token = "065f9f4243bba4c77f45014995fda349c0168f26"

class GiteaResponse(BaseModel):
    is_successful: bool
    data: dict

class CreateRepository(BaseModel):
    name: str

class CreateFile(BaseModel):
    content: str

class UpdateFile(BaseModel):
    content: str

class RenameRepo(BaseModel):
    new_name: str

class CreateUser(BaseModel):
    email: str = "user@example.com"
    full_name: str
    login_name: str
    must_change_password: bool = False
    password: str
    send_notify: bool = False
    username: str
    visibility: str = "public"