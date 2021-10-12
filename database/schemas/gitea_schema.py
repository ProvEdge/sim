from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

base_url = "https://gitea.provedge.cloud/api/v1"
access_token = "194e5b33eef95a4f905b4c28ede9bf8f76173b11"

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