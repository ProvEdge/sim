from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase
from database.schemas import instance_schema

gitea_server = "https://gitea.provedge.cloud"
base_url =  gitea_server + "/api/v1"
access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkZuNXBWWkZFRlVrbFR5Wk5zVkxOdzJ1MDh4Q2lfTFZjdHdHUUtuY0QxclEiLCJ0eXAiOiJKV1QifQ.eyJnbnQiOjUsInR0IjowLCJleHAiOjE2MzQ2NDk2MDYsImlhdCI6MTYzNDY0NjAwNn0.omUvwDt8xBbwpEoiucvMI_Tj8Sh8BxwIvj0B8_sIzA4QU3kvGQ7Fmfgkxz67Mm-uSQDvCan8RiYXOuAOtP6q6frCVa-AMnD1xtB68u4xXcyh-KiCxRgjhZgiKjRN89dktsmpdE8E8J0W5bHarEW58cxuKcVTfuwfAvUKWQWFiXNlaJD-V6vX1vjThEE90u912Fz1wGw0BWgEw2V6hPBfunjvPLFLQe1j34eL_ZgHF0B-vwA68SUBqh3w5ZQETD46ZVRrkLFtnRFfhp7pxdnlrOWuAAY0-_HnmoIMBHzy_YKVMCgMK4A0qssvrxY0rT460R0XyJLxkLiTmjtwklrFym0NnuTMP1bVg48lKnNDUpWmKhLAr9MqSp_tZWAO4PV_YAn3NrOOt9Y5MSmjAvvIvXYIWLbjGuBpKFFN4J2nF_sx60pk4wti3DfVxc1zOx0H-IJ1ZLPGY11zxKztX83R9EelCbWaYpZC6YhroKdoeREWLAFxQZEPQWTq65UmSlvlW_0zSpuGaAxRYWNQMa4B7OSTc7539CZ32_ktq0r0_w8WXIg0qAEZGywLmjIeBU6cjfXtewzsR8IBDa8Z3A9mTJRActSMEhmhKN7nViFjeiMPI0kgJ4kl4OnRcL5XKL-7sGz0AijkhE-xMTq9cpvTS7s0vcCpL16WAwYLFJaQU2I"
admin_access_token = "065f9f4243bba4c77f45014995fda349c0168f26"

class GiteaResponse(BaseModel):
    status_code: int
    data: dict

class CreateRepository(BaseModel):
    name: str



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


class CreateBranch(BaseModel):
    new_branch_name: str
    old_branch_name: str

class UpdateFile(BaseModel):
    content: str

class CreateFile(BaseModel):
    content: str

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

class ArgoConfiguration(BaseModel):
    argo_cluster: str = "https://kubernetes.default.svc"
    helm_path: str = "./jackal-base"

class InstanceCreate(BaseModel):
    name: str
    user_id: str
    belongs_to_group: bool
    group_id: str
    cluster_id: int
    robot_type: str = "jackal"
    argocd_project_name: str

class CreateInstance(BaseModel):
    instance: InstanceCreate
    helm: HelmValues
    argo: ArgoConfiguration