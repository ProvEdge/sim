from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

from database.schemas import argocd_schema

class GitResponse():
    def __init__(self, is_successful: bool, data: dict):
        self.is_successful = is_successful
        self.data = data

class HelmValues(BaseModel):
    namespace: str = "tunahan"
    cm_start_name: str = "jackal-start"
    cm_supervisord_name: str = "jackal-supervisord"
    dep_name: str = "jackal-1"
    replicas: int = 1
    http_port: int = 31001
    webrtc_port: int = 31002
    theia_port: int = 31003
    rosbridge_port: int = 31004
    webviz_port: int = 31005

class AddValuesToGit(BaseModel):
    access_token: str = "token"
    repo: str = "tunahanertekin/jackal-helm"
    filepath: str = "values/"
    helm_values: HelmValues
