from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase
from database.schemas import instance_schema

gitea_server = "https://gitea.provedge.cloud"
base_url =  gitea_server + "/api/v1"
access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkZuNXBWWkZFRlVrbFR5Wk5zVkxOdzJ1MDh4Q2lfTFZjdHdHUUtuY0QxclEiLCJ0eXAiOiJKV1QifQ.eyJnbnQiOjUsInR0IjowLCJleHAiOjE2MzQ2NDAxOTksImlhdCI6MTYzNDYzNjU5OX0.C9KoMsEIi_eUEZw6l-eJPWEWPfydMAti6RuiwOaw-kaNtQA1zhSu8b4v58VkpZ00TW8GfKUhTxeJu16UehzahzOWeTFPbno00lFXfukU4iKBHfSrFztbBiM49FDJIzrSeIItLgof6TUrrNasjFfSHbTPu_orpkcgppWlWXX32aVXfV8m4tUXcstRiy78fWgHDzA0IrYKMI76KM4d0tpXEFT5IKY2rlAVJfF4NYa6k-frpvy_bsv8ZvklXRDdPYT4FsIpZk4ny9LQWhCif8g09nd4Rbd95mCKSVMgO6TYoLbvmCbgbVvRVJfG2FWtXjmND2cRAkSckpy-ycpk4_imt_kIgYhCNl-EuMfwL4DsemMzjRKQDlQtsD7BbarhEjtX5TSTNME051LXiN5xbhlv7oMngn78AROmFXPwtfEAYcA5RhFHmWkDV2F6PGivWLcfSmJexcV2lll2U1NinzYBSyKBnjr8pw_z2_FUPFK_FDHrsL9oz7dHHUvU0hqEeA8wa0b7sRAaxv5DqI7tILvCF4Q00dgPa6W1NzNNfK7hmzeYPl1xLogTmxY7tF0raW6qB8zQ9RG9rOtRswIeSa_fa-O6jcVyDYxtaj1FREK0KtLVOnbRFbAEXHvUYsyVEO1I4Pq8oxt8aSP9TJFakY8RKJyZYvjILbBcFs_x7prriQk"
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
    helm_path: str = "."

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