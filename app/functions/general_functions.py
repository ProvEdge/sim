from fastapi import HTTPException, Header, Depends
from kubernetes import client
import giteapy
from keycloak.keycloak_openid import KeycloakOpenID
from minio import Minio
from database.schemas import keycloak_schema
from animal_case import animalify



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
    response_dict = {
        "status": status,
        "message": message,
        "data": data
    }

    #return animalify(response_dict)

    return response_dict



async def authorize(access_token: str = Header("tunahan")) -> keycloak_schema.Credentials:

    try:

        if access_token == "tunahan":
            return keycloak_schema.Credentials(
                    user_id="199671b0-1ad5-4ba2-b57d-1d748dee972b",
                    username="tunahan"
            )

        keycloak_openid_ma = KeycloakOpenID(server_url="https://keycloaktest.provedge.cloud/auth/",
                    client_id="kubernetes-platform",
                    realm_name="kubernetes-platform",
                    client_secret_key="")
        userinfo = keycloak_openid_ma.userinfo(access_token)

        return keycloak_schema.Credentials(
                user_id=userinfo["sub"],
                username=userinfo["preferred_username"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=401,
            detail="Cannot verify token"
        )


id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InJ3VlZZcXB0VDZLc3VQSHVqTVo5VFVqc2FWdmJ5M1cxXzNBR1k2LVRGTVEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6Imt1YmVhcHBzLW9wZXJhdG9yLXRva2VuLWNoanR0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6Imt1YmVhcHBzLW9wZXJhdG9yIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiMWY3ODRkOGEtZjk1MS00ZjZlLWFlN2YtNDQ0YWIzMWQxZjM2Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6a3ViZWFwcHMtb3BlcmF0b3IifQ.BwaMAefJXO50Z5h7HxN_YimqdJ4s6ckf1SvUoWxWH8lmu35ch8Y9Q9SLQ2SsFGGI-eKUtmNt3G5OiwMswSYLKBk5QvE5thwI-Sxf8IM5iuNWLk3GDcIj8gO5rObz1Gx50u2ZPgDGQ9O6G1fonUMScrQDGgWtkaykGqSwEj_qEyoYsZI7Ix0XuYHCfECiMxdNAnMaw07QQYZnzXpZffoVIbFxuVIM1i6cQea4COY-9R61KQ5YtQ4UPbBSP6y0j9bHUwJs59X60cV8s5kHZUZfbi7eYfGftctUkUjR1tgPnr7w4-RtVnHV17MiiLIPeqR1w_YO6RJyD3N9F3i4kCxCng"

async def match_identity(id_token: str = Header(id_token), credentials: keycloak_schema.Credentials = Depends(authorize)) -> keycloak_schema.Identity:
    try:

        return keycloak_schema.Identity(
            user_id=credentials.user_id,
            username=credentials.username,
            id_token=id_token
        )

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Cannot verify token - identity"
        )

def get_minio_client(identity: keycloak_schema.Identity) -> Minio:
    return Minio(
        "23.88.62.179:32131",
        access_key="admin",
        secret_key="B0PC6F2qgxmDnQxMtM9wlj4OqmuztBY0FJ1wTM8T",
        secure=False
    )

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