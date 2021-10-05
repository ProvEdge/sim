from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

class ArgoCDResponse():
    def __init__(self, status_code: int, data: dict):
        self.status_code = status_code
        self.data = data

class BearerTokenRequest(BaseModel):
    username: str
    password: str

class CreateApplicationRequest(BaseModel):
    name: str = "argo-app"
    #namespace: str
    cluster: str = "https://kubernetes.default.svc"
    helm_path: str = "."
    #repo_url: str = "https://github.com/tunahanertekin/jackal-helm"
    #values_file: str = "values.yaml"

class CreateApplicationResponse(ResponseBase):
    data: dict