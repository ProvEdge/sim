from datetime import datetime
from github.MainClass import Github
from pydantic.main import BaseModel
import requests, json
from requests.exceptions import Timeout
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.sqltypes import Time
from app.functions import git_rest_crud, instance_crud, usage_crud
from database.schemas import argocd_schema, instance_schema, platform_schema
from database.schemas.argocd_schema import ArgoCDResponse
from database.schemas.usage_schema import UsageCreate, UsageEdit

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
                        "selfHeal": True
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
        "revision": "HEAD",
        "prune": False,
        "dryRun": False,
        "strategy": {
            "hook": {
            "force": False
            }
        },
        "resources": None,
        "syncOptions": None
    }
    response =  requests.post(url=url, headers=auth_header, data=json.dumps(body), verify=False)

    status_code = response.status_code # response.status_code
    data = response.json()

    # data["metadata"].pop("managedFields")

    return ArgoCDResponse(
        status_code=status_code,
        data=data
    )


def refresh_argocd_application(app_name: str):
    url = argocd_server_url + "/applications/" + app_name + "?refresh=normal"

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

    response =  requests.get(url=url, headers=auth_header, verify=False)

    status_code = response.status_code # response.status_code
    data = response.json()

    return ArgoCDResponse(
        status_code=status_code,
        data=data
    )


def delete_argocd_application(
    db: Session,
    access_token: str, 
    instance_id: int
    ):

    db_instance = instance_crud.get_instance(db, instance_id)
    
    url = argocd_server_url + "/applications/" + db_instance.argocd_project_name
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

    response = requests.delete(url=url, headers=auth_header, verify=False)

    status_code = response.status_code
    data = response.json()

    delete_instance = {}
    if status_code == 200:
        delete_helm_values = git_rest_crud.delete_helm_values(
            access_token=access_token,
            repo_name=db_instance.values_repository,
            filepath=db_instance.values_path
        )

        delete_instance = instance_crud.delete_instance(db, instance_id)

    return ArgoCDResponse(
        status_code=status_code,
        data={
            "instance": delete_instance,
            "argocd": data
        }
    )



def start_instance(
    db: Session,
    access_token: str, 
    instance_id: int
):

    try:
        db_instance = instance_crud.get_instance(db, instance_id)

        values = {
            "deploymentReplicas": 1
        }

        edit_instance_values = git_rest_crud.edit_helm_values(
            access_token=access_token,
            repo_name=db_instance.values_repository,
            filepath=db_instance.values_path,
            values_content=values
        )

        refresh = {}
        if edit_instance_values.is_successful:
            refresh = refresh_argocd_application(db_instance.argocd_project_name)
            if refresh.status_code == 200:
                usage = UsageCreate(instance_id=db_instance.id)
                start_usage = usage_crud.create_usage(db, usage)
                return ArgoCDResponse(
                    status_code=200,
                    data={
                        "git": edit_instance_values.data,
                        "usage": start_usage,
                        "argocd": refresh.data
                    }
                )
        
        return ArgoCDResponse(
            status_code=400,
            data={
                "git": edit_instance_values.data,
                "argocd": {}
            }
        )

    except Exception as e:
        return ArgoCDResponse(
            status_code=400,
            data={
                "message": str(e)
            }
        )

    
def stop_instance(
    db: Session,
    access_token: str, 
    instance_id: int
):

    try:
        db_usages = usage_crud.get_usages(
            db,
            ins_id=instance_id,
            is_terminated=False
        )

        db_usage = db_usages[0]

        values = {
            "deploymentReplicas": 0
        }

        edit_instance_values = git_rest_crud.edit_helm_values(
            access_token=access_token,
            repo_name=db_usage.ins_values_repository,
            filepath=db_usage.ins_values_path,
            values_content=values
        )

        refresh = {}
        if edit_instance_values.is_successful:
            refresh = refresh_argocd_application(db_usage.ins_argocd_project_name)
            if refresh.status_code == 200:
                usage = UsageEdit(end_time=datetime.now(), is_terminated=True)
                edit_usage = usage_crud.edit_usage(db, db_usage.id, usage)
                return ArgoCDResponse(
                    status_code=200,
                    data={
                        "git": edit_instance_values.data,
                        "usage": edit_usage,
                        "argocd": refresh.data
                    }
                )
        
        return ArgoCDResponse(
            status_code=400,
            data={
                "git": edit_instance_values.data,
                "argocd": {}
            }
        )

    except Exception as e:
        return ArgoCDResponse(
            status_code=400,
            data={
                "message": str(e)
            }
        )

    