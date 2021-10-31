
from fastapi import Depends, APIRouter
from requests.sessions import Session

from database.schemas import keycloak_schema, kubeapps_schema, platform_schema

from app.functions import instance_crud, platform_ops
from app.functions.general_functions import generate_response, get_db, match_identity

router = APIRouter()

@router.get("/list-instances")
def list_instances(
    identity: keycloak_schema.Identity = Depends(match_identity)
):
    try:
        
        list_instances_req = platform_ops.list_instances(
            identity=identity
        )

        if list_instances_req.status_code == 200:
            return generate_response(
                "SUCCESS", 
                list_instances_req.message,
                list_instances_req.data
            )
        return generate_response(
            "FAILURE", 
            list_instances_req.message,
            list_instances_req.data
        )

    except Exception as e:
        return generate_response(
            status="FAILURE", 
            message=str(e)
        )


@router.post("/create-instance")
def create_instance(
    instance: platform_schema.CreateInstance,
    identity: keycloak_schema.Identity = Depends(match_identity),
    db: Session = Depends(get_db)
):
    try:
        
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
        return generate_response(
            "FAILURE", 
            create_instance_req.message,
            create_instance_req.data
        )

    except Exception as e:
        return generate_response(
            status="FAILURE", 
            message=str(e)
        )

@router.delete("/delete-instance/{instance}")
def delete_instance(
    instance: str,
    identity: keycloak_schema.Identity = Depends(match_identity),
    db: Session = Depends(get_db)
):
    try:
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
        return generate_response(
            "FAILURE", 
            delete_instance_req.message,
            delete_instance_req.data
        )

    except Exception as e:
        return generate_response(
            status="FAILURE", 
            message=str(e)
        )

@router.put("/update-instance/{instance}")
def update_instance(
    instance: str,
    values: dict, # define format
    identity: keycloak_schema.Identity = Depends(match_identity),
    db: Session = Depends(get_db)
):
    try:
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
        return generate_response(
            "FAILURE", 
            update_instance_req.message,
            update_instance_req.data
        )

    except Exception as e:
        return generate_response(
            status="FAILURE", 
            message=str(e)
        )


@router.post("/testing/{instance_id}")
def testing(
    instance_id: int,
    json_values: dict,
    identity: keycloak_schema.Identity = Depends(match_identity),
    db: Session = Depends(get_db)
):
    try:
        db_instance = instance_crud.get_instance(
            db=db,
            id=instance_id,
            credentials=keycloak_schema.Credentials(
                username=identity.username,
                user_id=identity.user_id
            )
        )

        x = platform_ops.generate_edited_yaml(
            json_values=json_values,
            instance=db_instance,
            db=db
        )

        print(x)


        return generate_response(
            "FAILURE", 
            ""
        )

    except Exception as e:
        return generate_response(
            status="FAILURE", 
            message=str(e)
        )