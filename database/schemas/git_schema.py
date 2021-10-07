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
    replicas: int = 0
    http_port: int = 31001
    webrtc_port: int = 31002
    theia_port: int = 31003
    rosbridge_port: int = 31004
    webviz_port: int = 31005

class AddValuesToGit(BaseModel):
    access_token: str = "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"
    repo: str = "tunahanertekin/jackal-helm"
    filepath: str = "values/"
    helm_values: HelmValues

class EditHelmValues(BaseModel):
    namespace: Optional[str]
    cm_start_name: Optional[str]
    cm_supervisord_name: Optional[str]
    dep_name: Optional[str]
    replicas: Optional[int]
    http_port: Optional[int]
    webrtc_port: Optional[int]
    theia_port: Optional[int]
    rosbridge_port: Optional[int]
    webviz_port: Optional[int]

class EditValues(BaseModel):
    access_token: str = "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"
    helm_values: EditHelmValues

class FileCommits(BaseModel):
    access_token: str = "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"
    repo: str = "tunahanertekin/jackal-helm"
    filepath: str = ""