from pydantic.main import BaseModel
import requests, json
from database.schemas import argocd_schema
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

def create_argocd_application(namespace: str, repo_url: str, values_path: str, application: argocd_schema.CreateApplicationRequest) -> ArgoCDResponse:

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
            "name": application.name
        },
        "spec": {
            "destination": {
            "name": "",
            "namespace": namespace,
            "server": application.cluster
            },
            "source": {
                "path": application.helm_path,
                "repoURL": "https://github.com/" + repo_url,
                "targetRevision": "HEAD",
                "helm": {
                    "valueFiles": [
                    values_path
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

    status_code = 0 # response.status_code
    data = response.json()

    # data["metadata"].pop("managedFields")

    return ArgoCDResponse(
        status_code=status_code,
        data=data
    )

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