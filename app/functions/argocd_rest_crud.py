from github.MainClass import Github
from pydantic.main import BaseModel
import requests, json
from requests.exceptions import Timeout
from sqlalchemy.orm.session import Session
from app.functions import instance_crud
from database.schemas import argocd_schema, instance_schema, platform_schema
from database.schemas.argocd_schema import ArgoCDResponse

argocd_server_url = "https://localhost:8080/api/v1"

def get_bearer_token(credentials: argocd_schema.BearerTokenRequest) -> ArgoCDResponse:
    url = argocd_server_url + "/session"

    response =  requests.post(url=url, data=json.dumps(credentials), verify=False)

    status_code = response.status_code
    data = response.json()

    return ArgoCDResponse(
        status_code=status_code,
        data=data
    )

def create_argocd_application(
    db: Session,
    access_token: str,
    argo_cluster: str,
    helm_path: str,
    instance: instance_schema.InstanceCreate
) -> ArgoCDResponse:

    try:

        g = Github(access_token)
        repo = g.get_repo(instance.values_repository)
        file_content = repo.get_contents(instance.values_path).decoded_content

        url = argocd_server_url + "/applications"
        token_res = get_bearer_token(
            {
                "username": "admin",
                "password": "ncHjjNs7De47HaMm"
            }
        )
        token = token_res.data["token"]
        auth_header = {
            "Cookie": "argocd.token=" + token
        }

        body = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "Application",
            "metadata": {
                "name": instance.argocd_project_name
            },
            "spec": {
                "destination": {
                "name": "",
                "namespace": instance.namespace,
                "server": argo_cluster
                },
                "source": {
                    "path": helm_path,
                    "repoURL": "https://github.com/" + instance.values_repository,
                    "targetRevision": "HEAD",
                    "helm": {
                        "valueFiles": [
                        instance.values_path
                        ]
                    }
                },
                "project": "default",
                "syncPolicy": {
                    "automated": {
                        "prune": False,
                        "selfHeal": False
                    }
                }
            }
        }

        response =  requests.post(url=url, headers=auth_header, data=json.dumps(body), verify=False)
        status_code = response.status_code
        data = response.json()

        instance_db = {}
        if status_code == 200:
            instance_db = instance_crud.create_instance(db, instance)

        return ArgoCDResponse(
            status_code=status_code,
            data={
                "instance": instance_db,
                "argocd": data
            }
        )
    except Exception as e:
        # clear all
        return ArgoCDResponse(
            status_code=0,
            data={
                "message": str(e)
            }
        )

    

    # try:
    #     response =  requests.post(url=url, headers=auth_header, data=json.dumps(body), verify=False, timeout=2)
    #     status_code = 0 # response.status_code
    #     data = response.json()

    #     return ArgoCDResponse(
    #         status_code=status_code,
    #         data=data
    #     )
    # except Timeout:
    #     return ArgoCDResponse(
    #         status_code=400,
    #         data={
    #             "message": "ArgoCD request has timed out"
    #         }
    #     )

    

def sync_argocd_application(app_name: str):
    url = argocd_server_url + "/applications/" + app_name + "/sync"

    token_res = get_bearer_token(
        {
            "username": "admin",
            "password": "ncHjjNs7De47HaMm"
        }
    )

    token = token_res.data["token"]

    auth_header = {
        "Cookie": "argocd.token=" + token
    }

    body = {
        "dryrun": True
    }

    response =  requests.post(url=url, headers=auth_header, data=json.dumps(body), verify=False)

    status_code = response.status_code # response.status_code
    data = response.json()

    # data["metadata"].pop("managedFields")

    return ArgoCDResponse(
        status_code=status_code,
        data=data
    )


def delete_argocd_application(app_name: str):
    url = argocd_server_url + "/applications/" + app_name
    token_res = get_bearer_token(
        {
            "username": "admin",
            "password": "ncHjjNs7De47HaMm"
        }
    )
    token = token_res.data["token"]
    auth_header = {
        "Cookie": "argocd.token=" + token
    }

    response =  requests.delete(url=url, headers=auth_header, verify=False)

    status_code = response.status_code
    data = response.json()

    return ArgoCDResponse(
        status_code=status_code,
        data=data
    )