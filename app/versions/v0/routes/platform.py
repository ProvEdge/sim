from typing import Optional, Union

from fastapi import APIRouter, Header

from app import models
from database.schemas import argocd_schema, generic, platform_schema, git_schema

from app.functions import argocd_rest_crud, git_rest_crud, kubernetes_jobs
from app.functions.general_functions import generate_response

import yaml, json

from github import Github

router = APIRouter()

from database.schemas import generic

    


@router.post("/create-instance")
def create_instance(instance: platform_schema.CreateInstance):

    try:
        create_values = git_rest_crud.add_instance_values(
            access_token=instance.gitops.access_token,
            repo_name=instance.gitops.repo,
            filepath=instance.gitops.filepath,
            values_content=instance.gitops.helm_values
        )

        if create_values.is_successful:
            create_argo_app = argocd_rest_crud.create_argocd_application(
                namespace=instance.gitops.helm_values.namespace,
                repo_url=instance.gitops.repo,
                values_path=instance.gitops.filepath,
                application=instance.argocd_app
            )
            return generate_response(
                "SUCCESS",
                "ArgoCD app is created",
                create_argo_app.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot make Git operation",
                create_values.data
            )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.post("/edit-instance-values")
def edit_instance(instance: platform_schema.CreateInstance):

    try:
        edit_values = git_rest_crud.edit_helm_values(
            access_token=instance.gitops.access_token,
            repo_name=instance.gitops.repo,
            filepath=instance.gitops.filepath,
            values_content=instance.gitops.helm_values
        )

        if edit_values.is_successful:
            return generate_response(
                "SUCCESS",
                "Git operation is successful",
                edit_values.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot make Git operation",
                edit_values.data
            )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )



@router.get("/sync-instance/{instance_id}")
def sync_instance(instance_id: str):

    # turn argocd app name to instance id

    try:
        sync_req = argocd_rest_crud.sync_argocd_application(instance_id)

        if sync_req.status_code == 200:
            return generate_response(
                "SUCCESS",
                "Instance sync is successful",
                sync_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot sync the instance",
                sync_req.data
            )
    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )




@router.post("/bearer", deprecated=True)
def bearer(credentials: argocd_schema.BearerTokenRequest):

    res = argocd_rest_crud.get_bearer_token(credentials=credentials)

    return {
        "data": res
    }


@router.post("/create-argocd-app", deprecated=True, response_model=Union[argocd_schema.CreateApplicationResponse, generic.ResponseBase])
def create_argocd_application(application: argocd_schema.CreateApplicationRequest, APIServer: str = Header(None), Token: str = Header(None)):
    
    try:
        resp = argocd_rest_crud.create_argocd_application(application=application)
        return generate_response(
            "SUCCESS",
            "ArgoCD app is created",
            resp.data
        )
    except Exception as e:
        return generate_response(
            "FAILURE",
            "An error occurred"
        )


@router.post("/create-values-yaml", deprecated=True, response_model=Union[dict, generic.ResponseBase])
def create_values_yaml(credentials: git_schema.AddValuesToGit):

    try:
        
        create_values = git_rest_crud.add_instance_values(
            access_token=credentials.access_token,
            repo=credentials.repo,
            filepath=credentials.filepath,
            values_content=credentials.helm_values
        )

        
        
        return create_values.data
    except Exception as e:
        return {
            "ex": str(e)
        }