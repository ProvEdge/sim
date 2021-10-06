from typing import Optional, Union

from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm.session import Session

from app import models
from database.schemas import argocd_schema, generic, platform_schema, git_schema

from app.functions import argocd_rest_crud, git_rest_crud, instance_crud, kubernetes_jobs
from app.functions.general_functions import generate_response, get_db

from database.database import engine

models.Base.metadata.create_all(bind=engine)


router = APIRouter()

from database.schemas import generic

@router.post("/create-values-yaml")
def create_values_yaml(values: git_schema.AddValuesToGit):
    try:
        create_values = git_rest_crud.add_instance_values(
            access_token=values.access_token,
            repo_name=values.repo,
            filepath=values.filepath,
            values_content=values.helm_values
        )

        if create_values.is_successful:
            return generate_response(
                "SUCCESS",
                "Values yaml is generated, " + values.filepath
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


@router.post("/create-instance")
def create_instance(instance: platform_schema.CreateInstance, db: Session = Depends(get_db)):

    try:
        create_argo_app = argocd_rest_crud.create_argocd_application(
            db=db,
            access_token=instance.access_token,
            argo_cluster=instance.argo_cluster,
            helm_path=instance.helm_path,
            instance=instance.instance
        )

        if create_argo_app.status_code == 200:
            return generate_response(
                "SUCCESS",
                "ArgoCD app is created",
                create_argo_app.data
            )
        else: return generate_response(
            "FAILURE",
            "Problem when creating ArgoCD app",
            create_argo_app.data
        )

    except Exception as e:
        return generate_response(
            "FAILURE",
            str(e)
        )


@router.post("/edit-instance")
def edit_instance(values: git_schema.EditValues):

    try:
        edit_values = git_rest_crud.edit_helm_values(
            access_token=values.access_token,
            repo_name=values.repo,
            filepath=values.filepath,
            values_content=values.helm_values
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


@router.delete("/delete/{instance_id}")
def delete_instance(instance_id: int, credentials: platform_schema.DeleteInstance, db: Session = Depends(get_db)):

    try:
        
        delete_req = argocd_rest_crud.delete_argocd_application(
            db=db,
            access_token=credentials.access_token,
            instance_id=instance_id
        )

        if delete_req.status_code == 200:
            return generate_response(
                "SUCCESS",
                "Instance deletion is successful",
                delete_req.data
            )
        else:
            return generate_response(
                "FAILURE",
                "Cannot delete the instance",
                delete_req.data
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


# @router.post("/create-values-yaml", deprecated=True, response_model=Union[dict, generic.ResponseBase])
# def create_values_yaml(credentials: git_schema.AddValuesToGit):

#     try:
        
#         create_values = git_rest_crud.add_instance_values(
#             access_token=credentials.access_token,
#             repo=credentials.repo,
#             filepath=credentials.filepath,
#             values_content=credentials.helm_values
#         )

        
        
#         return create_values.data
#     except Exception as e:
#         return {
#             "ex": str(e)
#         }