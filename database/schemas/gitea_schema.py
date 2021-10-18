from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase
from database.schemas import instance_schema

gitea_server = "https://gitea.provedge.cloud"
base_url =  gitea_server + "/api/v1"
access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkZuNXBWWkZFRlVrbFR5Wk5zVkxOdzJ1MDh4Q2lfTFZjdHdHUUtuY0QxclEiLCJ0eXAiOiJKV1QifQ.eyJnbnQiOjUsInR0IjowLCJleHAiOjE2MzQ1OTUyNTQsImlhdCI6MTYzNDU5MTY1NH0.VXkIIHYY9c_Cz0F5uJFBl06RcZtgC14R7B2PRbxNVCZZTWwBLXOv8OcRfOLAPVTfg9IJJ3pkigyujgR-kEj0IflonIbENqzS1EoExYebo0aeypTRpOgo1nJcPyxXTvPuYuTnU9bop3osuzNKBPnybiyexYL0ROw0QgIKrS-kqx217TzJGD7PUxEc_RsFdihy5S4y1x_utyAuWPB8Foymtdku_aqHuCUhLib9Y_rohkFJVVl8ZYG4grXNEcX6qIQvtD2G1UbX0Nt1HOGD9lFSbsax1xBmPi1Qbf1NSSf-9OOgoUao_yKVoJEAJlqjZ1kSe2ZjUVobGIdK_ey3Xm_YxROmqGrVxaZDuG4AmfzzAk6r9FXUIeWHSNZylXgaB_nZpp-UM4Iof2Pbq9xZCwooTyieHNRF684nLEKMUc5-uB5J9wUBUnV1YBa_tUQ11BToMbWtBuataAc6msSgMARQv1Z0i2clJjzRyzG_v8ZplqPhYbtrxUHhpWasH49bs5LEHjjzEymfDoT-972kKad47lY7TNn25lQhZLuWdD2wrXilnrzzV4c84e2HeHFNJxMqYXMF50AqrOIcjWoGldXzx1DcU0VgptEBXrkX4J0ypNoYhaWz7QXkdG9GpI3z26SzxJTTdP1bTP_lGFIBucejHz_s6k1BG0xBIIlnuQjsgt4"
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