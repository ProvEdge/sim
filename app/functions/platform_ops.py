import yaml, json
from sqlalchemy.orm.session import Session
from database.schemas import instance_schema, kubeapps_schema, platform_schema, keycloak_schema
from database.schemas.platform_schema import PlatformResponse

from app.functions import instance_crud, kubeapps_rest_crud, robot_crud

def list_instances(
    identity: keycloak_schema.Identity
) -> PlatformResponse:

    get_releases_req = kubeapps_rest_crud.get_releases_by_namespace(
        id_token=identity.id_token,
        namespace=identity.username
    )

    if get_releases_req.status_code == 200:
        return PlatformResponse(
            status_code=200,
            message="Releases (namespaced) are listed",
            data=get_releases_req.data
        )

    return PlatformResponse(
            status_code=400,
            message="Cannot get releases from Kubeapps",
            data={}
        )
    


def create_instance(
    identity: keycloak_schema.Identity,
    name: str,
    robot_type: str,
    db: Session
) -> PlatformResponse:

    try:
        robot_db = robot_crud.get_robot(
            db=db,
            type=robot_type
        )

        create_kubeapps_release_req = kubeapps_rest_crud.post_release(
            id_token=identity.id_token,
            namespace=identity.username,
            release=kubeapps_schema.CreateRelease(
                appRepositoryResourceName=robot_db.app_repository,
                appRepositoryResourceNamespace=robot_db.app_repository_namespace,
                chartName=robot_db.chart_name,
                version=robot_db.chart_version,
                releaseName=name,
                values=robot_db.helm_values
            )
        )

        if create_kubeapps_release_req.status_code == 200:
            create_instance_req = instance_crud.create_instance(
                db=db,
                instance=instance_schema.InstanceCreate(
                    name=name,
                    namespace=identity.username,
                    robot_type=robot_type,
                    release_name=name,
                    helm_values=manipulate_values(
                        helm_values=robot_db.helm_values,
                        identity=identity
                    )
                ),
                credentials=keycloak_schema.Credentials(
                    username=identity.username,
                    user_id=identity.user_id
                )
            )


            return PlatformResponse(
                status_code=200,
                message="Instance is being created",
                data={
                    "instance": create_instance_req,
                    "kubeapps": create_kubeapps_release_req.data
                }
            )

        return PlatformResponse(
            status_code=400,
            message="Cannot create instance",
            data=create_kubeapps_release_req.data
        )

    except Exception as e:
        return PlatformResponse(
            status_code=400,
            message=str(e),
            data={}
        )

def delete_instance(
    identity: keycloak_schema.Identity,
    name: str,
    db: Session
) -> PlatformResponse:

    try:
        instance_db = instance_crud.get_instance_by_name(
            db=db,
            name=name,
            credentials=keycloak_schema.Credentials(
                username=identity.username,
                user_id=identity.user_id
            )
        )

        delete_kubeapps_release_req = kubeapps_rest_crud.delete_release(
            id_token=identity.id_token,
            namespace=identity.username,
            release=instance_db.release_name
        )

        if delete_kubeapps_release_req.status_code == 200:
            delete_instance_req = instance_crud.delete_instance(
                db=db,
                id=instance_db.id,
                credentials=keycloak_schema.Credentials(
                    username=identity.username,
                    user_id=identity.user_id
                )
            )

            return PlatformResponse(
                status_code=200,
                message="Instance is being deleted",
                data={
                    "instance": delete_instance_req,
                    "kubeapps": delete_kubeapps_release_req.data
                }
            )

        else: 
            return PlatformResponse(
                status_code=400,
                message="Cannot delete instance",
                data=delete_kubeapps_release_req.data
            )
    except Exception as e:
        return PlatformResponse(
            status_code=400,
            message=str(e),
            data={}
        )

    

    
# replace it with smarter helm value picker !
def manipulate_values(helm_values: str, identity: keycloak_schema.Identity):
    received_yaml = yaml.safe_load(helm_values)
    received_yaml["namespace"] = identity.username
    converted_yaml = yaml.dump(received_yaml, allow_unicode=True)
    return converted_yaml





    