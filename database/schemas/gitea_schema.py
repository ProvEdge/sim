from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

base_url = "https://gitea.provedge.cloud/api/v1"
access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkZuNXBWWkZFRlVrbFR5Wk5zVkxOdzJ1MDh4Q2lfTFZjdHdHUUtuY0QxclEiLCJ0eXAiOiJKV1QifQ.eyJnbnQiOjQsInR0IjowLCJleHAiOjE2MzQyNTQ5MjcsImlhdCI6MTYzNDI1MTMyN30.AD6d6p-aGzHEwUMTvKEkN7DWuti8O5Quv-rV6iqA2PErcr1lQc0dHfkQ9doXD5S1NCuFvnaoKx1cqr3WSXMmOAhfQyFl-0n1KeZe1ddOOoKl_tS81wv1jGQDFvflRDJ8-IWmLa0VMlD7A2VdK04XVNx1xH7nkVWhwt4Dst81QzLOCykbLAP3EMHokZCOHAkqZEffHpFoOqYQqYChWbnecNem2DVI-fDNpxZRfiGNzrQ6OEMr23aNb3pSU82JxvjnMUqujKO40KiGkGULDQNldpwGbgMs34q-eKGpLdLry9oC87tkFPc25qBT2WOL6J4EctsA7VrE4E4N5ogi7pPeKirbEkrcAOWge_Qqrt5Auml4V8wAUpyKQUjauqMDHC4APj9wHjjd36Hwk19a_zaWhqhWgNI6h54sZwNmFfUryRvx5zKXHiXfZQq8vqp2jEBqazpySsZBRYPH6AEBB-x9Dz0MK-6kXohOKw-Bz-L2hpjoVMrpsP5xrc5SB1mWPNzf_k4GJ9MA1Vc8qR_c_ShFvpd2cvexPVL0bqiQZqwzfkWe2KeWi_Id-eUq94EvinebbJ0LueIjRsV-xCTWhsk6-0ociWqr16loWD1MLhSeOWmMmX3koR-OEZb-0fWm0d6yR2RjfomKGJ_2XkWvAN27_vyie_0Z2l8Dy9GzPLy9dr0"
admin_access_token = "065f9f4243bba4c77f45014995fda349c0168f26"

class GiteaResponse(BaseModel):
    status_code: int
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


class CreateBranch(BaseModel):
    new_branch_name: str
    old_branch_name: str