from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

base_url = "https://gitea.provedge.cloud/api/v1"
access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkZuNXBWWkZFRlVrbFR5Wk5zVkxOdzJ1MDh4Q2lfTFZjdHdHUUtuY0QxclEiLCJ0eXAiOiJKV1QifQ.eyJnbnQiOjQsInR0IjowLCJleHAiOjE2MzQzMDMzMTYsImlhdCI6MTYzNDI5OTcxNn0.GdYlQ928nnre9O1ASprKpBySzugO-6blvcMD8gjwaVF0QaZaSVA66TKvMkfrArtezhxFgJfcwG4RIToSqpeiERZ5y6mbM1XP110giHoVEbgxVFL3OEPNWB4fzyQrmJvqEgwsHZbWeX8Fq94AQfHT-D3_cDBsFYLFCqQdoY9CFni-PfvFK2qTLCeNtfuY_jZe8ieSw034gFDqTIVg5vCkjCBHIF0pfB6E2Ijb32WsrAlK38A6Z62e9kY8dE27RuaVM7J-Z0HpGIxijVATV5y4S7y0BqR4q3Qkt_sgLdYglfcvRXqu7X9__ha7vuf-8LJE0zCuawUwe-E_yMq-3EUhcpwAqQ0ePJxl7PFwbL3JJzTEOCJPhtCzzdgbX3ia5axLkofdDLAQqrafSsS3-1bzruyoz7LbNmIp3yrN-oz4_Bpzov4em3fssguKCEdcywJTebMqK8ZuZ4Ltm-nxzND9aLUFigoAqsm2pHssggg3uK5Xi6-pOc9akfZ6VTbXn7s9MPmC3dvUQTQ4Tt2H1QawpHjUlw83jg9keqxECTwuFrdSQt-0UBBKxvacdrNjbaqtCP039VHp2kzONl4oxBM9IQcH3jTlMfo99neEIWJcmQe-lxH8Y2CQmDp72_-M97TKwJ5CXP72hInnr07e47QAM8WQkCTCQoQfhn2JRL6zV6A"
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