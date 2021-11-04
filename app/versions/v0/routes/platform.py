
from typing import Union
from fastapi import Depends, APIRouter
from fastapi.exceptions import HTTPException
from requests.sessions import Session
from starlette.responses import JSONResponse

from database.schemas import keycloak_schema, kubeapps_schema, platform_schema

from app.functions import instance_crud, platform_ops
from app.functions.general_functions import generate_response, get_db, get_minio_client, match_identity

router = APIRouter()

@router.get(
    path="/list-instances",
    response_model=platform_schema.ListReleasesResponse
)
def list_instances(
    identity: keycloak_schema.Identity = Depends(match_identity)
):
        
    list_instances_req = platform_ops.list_instances(
        identity=identity
    )

    if list_instances_req.status_code == 200:
        return generate_response(
            "SUCCESS", 
            list_instances_req.message,
            list_instances_req.data
        )

    return JSONResponse(
        status_code=404,
        content=generate_response(
            "FAILURE",
            list_instances_req.message,
            list_instances_req.data
        )
    )

    


@router.post(
    path="/create-instance",
    response_model=platform_schema.CreateReleaseResponse
)
def create_instance(
    instance: platform_schema.CreateInstance,
    identity: keycloak_schema.Identity = Depends(match_identity),
    db: Session = Depends(get_db)
):
    create_instance_req = platform_ops.create_instance(
        identity=identity,
        name=instance.name,
        robot_type=instance.robot_type,
        db=db
    )

    if create_instance_req.status_code == 200:
        return generate_response(
            "SUCCESS", 
            create_instance_req.message,
            create_instance_req.data
        )

    return JSONResponse(
        status_code=406,
        content=generate_response(
            "FAILURE",
            create_instance_req.message,
            create_instance_req.data
        )
    )


@router.delete(
    path="/delete-instance/{instance}",
    response_model=platform_schema.DeleteReleaseResponse
)
def delete_instance(
    instance: str,
    identity: keycloak_schema.Identity = Depends(match_identity),
    db: Session = Depends(get_db)
):
    delete_instance_req = platform_ops.delete_instance(
        identity=identity,
        name=instance,
        db=db
    )

    if delete_instance_req.status_code == 200:
        return generate_response(
            "SUCCESS", 
            delete_instance_req.message,
            delete_instance_req.data
        )
    
    return JSONResponse(
        status_code=delete_instance_req.status_code,
        content=generate_response(
            "FAILURE",
            delete_instance_req.message,
            delete_instance_req.data
        )
    )
    

@router.put(
    path="/update-instance/{instance}",
    response_model=platform_schema.UpdateReleaseResponse
)
def update_instance(
    instance: str,
    values: dict, # define format
    identity: keycloak_schema.Identity = Depends(match_identity),
    db: Session = Depends(get_db)
):
    update_instance_req = platform_ops.update_instance(
        name=instance,
        json_values=values,
        identity=identity,
        db=db
    )

    if update_instance_req.status_code == 200:
        return generate_response(
            "SUCCESS", 
            update_instance_req.message,
            update_instance_req.data
        )

    return JSONResponse(
        status_code=update_instance_req.status_code,
        content=generate_response(
            "FAILURE",
            update_instance_req.message,
            update_instance_req.data
        )
    )
    


@router.get(
    path="/start-instance/{instance}",
    response_model=platform_schema.UpdateReleaseResponse
)
def start_instance(
    instance: str,
    identity: keycloak_schema.Identity = Depends(match_identity),
    db: Session = Depends(get_db)
):

    replica_count = 1

    update_instance_req = platform_ops.update_instance(
        name=instance,
        json_values={
            "deploymentReplicas": replica_count
        },
        identity=identity,
        db=db
    )

    if update_instance_req.status_code == 200:
        return generate_response(
            "SUCCESS", 
            "Instance is started, replica count is " + str(replica_count),
            update_instance_req.data
        )

    return JSONResponse(
        status_code=update_instance_req.status_code,
        content=generate_response(
            "FAILURE",
            update_instance_req.message,
            update_instance_req.data
        )
    )


@router.get(
    path="/stop-instance/{instance}",
    response_model=platform_schema.UpdateReleaseResponse
)
def stop_instance(
    instance: str,
    identity: keycloak_schema.Identity = Depends(match_identity),
    db: Session = Depends(get_db)
):
    replica_count = 0

    update_instance_req = platform_ops.update_instance(
        name=instance,
        json_values={
            "deploymentReplicas": replica_count
        },
        identity=identity,
        db=db
    )

    if update_instance_req.status_code == 200:
        return generate_response(
            "SUCCESS", 
            "Instance is started, replica count is " + str(replica_count),
            update_instance_req.data
        )

    return JSONResponse(
        status_code=update_instance_req.status_code,
        content=generate_response(
            "FAILURE",
            update_instance_req.message,
            update_instance_req.data
        )
    )



# @router.get("/minio-test")
# def minio_test(
#     identity: keycloak_schema.Identity = Depends(match_identity)
# ):
#     try:
#         import io
#         client = get_minio_client(
#             identity=identity
#         )

#         b = client.list_buckets()
        
#         xstr = "hello"
#         client.put_object(
#             bucket_name="second",
#             object_name="x.yaml",
#             data=io.BytesIO(bytes(xstr, 'utf-8')),
#             length=len(xstr),
#             content_type="application/x-yaml"
#         )

#         content = client.get_object("second", "x.yaml")
        
#         return generate_response(
#             "FAILURE", 
#             "musi",
#             content
#         )

#     except Exception as e:
#         return generate_response(
#             status="FAILURE", 
#             message=str(e)
#         )

