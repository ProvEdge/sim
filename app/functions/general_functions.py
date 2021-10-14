from typing import Optional
from fastapi import HTTPException
from kubernetes import client
import giteapy


def get_db():
    from database.database import SessionLocal, engine

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_response(status: str, message: str, data = {}):
    # if status == "FAILURE":
    #     raise HTTPException(status_code=400, detail=message)
    return {
        "status": status,
        "message": message,
        "data": data
    }


def get_k8s_api_client(host_url: str, bearer_token: str) -> client.ApiClient:
    if bearer_token == "admin": # should be admin token
        bearer_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InJ3VlZZcXB0VDZLc3VQSHVqTVo5VFVqc2FWdmJ5M1cxXzNBR1k2LVRGTVEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrdWJlY29uZmlnLXNhLXRva2VuLWhybGQ4Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6Imt1YmVjb25maWctc2EiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiIxN2Y3MWM5Mi04NTZhLTQ2N2ItYTdiYi0xYTZkZTJlZjNiYWYiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06a3ViZWNvbmZpZy1zYSJ9.L54YtaMlLA5OlTcCb_eR35jWyz7dutHJjzKiKrmodMzK6I2msYPbftP-I25vwbILf6GNd4Xt41QBJm_Kjavfz6ZvLdBlZeAbsbK5izLt526TGzGTZWcgyX2W-eknBlm0MB8wIv0lG6LPGLKqMieV97cY8ri-5WS9efdF2AeGYd2YJP_B-WwhuZR1cY6G4u0JL3xWBRdKaRbSaYFkuOErb6I1AQVIQT0lZrd2GmZ5JkqI1odQJpG5GFp0KkkN8iCNIh31s3rI2petGXrReLdsIeWzppwUkBFjIRuzd_K2f_iaQds8GAXYlNjWbnIcB-AeyaLwV5yLvsvF2SRrgYWK1g"
    if host_url == "admin":
        host_url = "https://167.233.13.71:6443"
    
    conf = client.Configuration(
        host=host_url,
        api_key={"authorization": "Bearer " + bearer_token},
    )
    conf.verify_ssl = False
    api_client = client.ApiClient(conf)

    return api_client

def gitea_repo_api(url: str, access_token: str):

    conf = giteapy.Configuration()
    conf.api_key["Authorization"] = access_token
    conf.get_api_key_with_prefix["Authorization"] = "Bearer"
    conf.host = url

    repo_api = giteapy.RepositoryApi(
        api_client=giteapy.ApiClient(conf)
    )

    return repo_api


def gitea_user_api(url: str, access_token: str):

    conf = giteapy.Configuration()
    conf.api_key["Authorization"] = access_token
    conf.api_key_prefix["Authorization"] = "Bearer"
    conf.host = url

    user_api = giteapy.UserApi(
        api_client=giteapy.ApiClient(conf)
    )

    return user_api


def gitea_admin_api(url: str, access_token: str):

    conf = giteapy.Configuration()
    conf.api_key["access_token"] = access_token
    conf.host = url

    admin_api = giteapy.AdminApi(
        api_client=giteapy.ApiClient(conf)
    )

    return admin_api