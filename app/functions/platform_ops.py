from minio.commonconfig import ENABLED
import yaml, io

from sqlalchemy.orm.session import Session
from app.functions.general_functions import get_minio_client
from minio.versioningconfig import VersioningConfig
from database.schemas import instance_schema, kubeapps_schema, platform_schema, keycloak_schema
from database.schemas import platform_schema
from database.schemas.platform_schema import DeleteReleaseInstanceStatus, DeleteReleaseKubeappsStatus, PlatformResponse
from app.functions import instance_crud, kubeapps_rest_crud, robot_crud

def list_instances(
    identity: keycloak_schema.Identity
) -> platform_schema.PlatformResponse:

    
    get_releases_req = kubeapps_rest_crud.get_releases_by_namespace(
        id_token=identity.id_token,
        namespace=identity.username
    )

    if get_releases_req.status_code == 200:
        releases = platform_schema.ListReleasesResponseData.parse_obj(get_releases_req.data)

        return platform_schema.PlatformResponse(
            status_code=200,
            message="Releases (namespaced) are listed",
            data=releases.dict()
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
) -> platform_schema.PlatformResponse:

    
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
            values=manipulate_values(
                helm_values=robot_db.helm_values,
                identity=identity
            )
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

        minio_client = get_minio_client(
            identity=identity
        )

        if minio_client.bucket_exists(identity.username) == False:
            minio_client.make_bucket(
                bucket_name=identity.username
            )

        values_str = str(manipulate_values(
            helm_values=robot_db.helm_values,
            identity=identity
        ))
        
        minio_req = minio_client.put_object(
            bucket_name=identity.username,
            object_name="instance_" + str(create_instance_req.id) + ".yaml",
            data=io.BytesIO(bytes(values_str, 'utf-8')),
            length=len(values_str),
            content_type="application/x-yaml"
        )

        # control minio response

        create_release_response_data = platform_schema.CreateReleaseResponseData(
            creation_status=platform_schema.CreateReleaseStatus(
                instance=platform_schema.CreateReleaseInstanceStatus(
                    success=True,
                    message="Instance record is created in database."
                ),
                kubeapps=platform_schema.CreateReleaseKubeappsStatus(
                    success=True,
                    message="Kubeapps release is created."
                ),
                minio=platform_schema.CreateReleaseMinioStatus(
                    success=True,
                    message="MinIO values injection is added."
                )
            )
        )

        return PlatformResponse(
            status_code=200,
            message="Instance is being created",
            data=create_release_response_data.dict()
        )

    create_release_response_data = platform_schema.CreateReleaseResponseData(
        creation_status=platform_schema.CreateReleaseStatus(
            instance=platform_schema.CreateReleaseInstanceStatus(
                success=False,
                message="Upper Error."
            ),
            kubeapps=platform_schema.CreateReleaseKubeappsStatus(
                success=False,
                message=str(create_kubeapps_release_req.data)
            ),
            minio=platform_schema.CreateReleaseMinioStatus(
                success=False,
                message="Upper Error"
            )
        )
    )

    return PlatformResponse(
        status_code=406,
        message="Cannot create instance",
        data=create_release_response_data.dict()
    )

   

def delete_instance(
    identity: keycloak_schema.Identity,
    name: str,
    db: Session
) -> PlatformResponse:

    instance_db = instance_crud.get_instance_by_name(
        db=db,
        name=name,
        credentials=keycloak_schema.Credentials(
            username=identity.username,
            user_id=identity.user_id
        )
    )

    if instance_db is None:
        return PlatformResponse(
            status_code=404,
            message="Instance not found.",
            data={}
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

        delete_release_response_data = platform_schema.DeleteReleaseResponseData(
            deletion_status=platform_schema.DeleteReleaseStatus(
                instance=DeleteReleaseInstanceStatus(
                    success=True,
                    message="Instance is deleted."
                ),
                kubeapps=DeleteReleaseKubeappsStatus(
                    success=True,
                    message="Kubeapps release is deleted."
                )
            )
        )


        return PlatformResponse(
            status_code=200,
            message="Instance is being deleted",
            data=delete_release_response_data.dict()
        )

    else: 
        delete_release_response_data = platform_schema.DeleteReleaseResponseData(
            deletion_status=platform_schema.DeleteReleaseStatus(
                instance=DeleteReleaseInstanceStatus(
                    success=False,
                    message="Upper error."
                ),
                kubeapps=DeleteReleaseKubeappsStatus(
                    success=False,
                    message="Kubeapps release cannot be deleted."
                )
            )
        )
        return PlatformResponse(
            status_code=406,
            message="Cannot delete instance",
            data=delete_kubeapps_release_req.data
        )


def update_instance(
    identity: keycloak_schema.Identity,
    name: str,
    json_values: dict,
    db: Session
) -> PlatformResponse:

    instance_db = instance_crud.get_instance_by_name(
        db=db,
        name=name,
        credentials=keycloak_schema.Credentials(
            username=identity.username,
            user_id=identity.user_id
        )
    )

    robot_db = robot_crud.get_robot(
        db=db,
        type=instance_db.robot_type
    )

    is_valid, edited_yaml = generate_edited_yaml(
        json_values=json_values,
        instance=instance_db,
        db=db
    )

    if is_valid == False:
        return PlatformResponse(
            status_code=400,
            message="Values are not valid, follow the format: " + robot_db.helm_values,
            data={}
        )

    update_kubeapps_release_req = kubeapps_rest_crud.update_release(
        id_token=identity.id_token,
        namespace=identity.username,
        release_name=instance_db.release_name,
        release=kubeapps_schema.UpdateRelease(
            appRepositoryResourceName=robot_db.app_repository,
            appRepositoryResourceNamespace=robot_db.app_repository_namespace,
            chartName=robot_db.chart_name,
            values=edited_yaml
        )
    )

    if update_kubeapps_release_req.status_code == 200:

        edit_instance_req = instance_crud.edit_instance(
            db=db,
            id=instance_db.id,
            instance=instance_schema.InstanceEdit(
                helm_values=edited_yaml
            ),
            credentials=keycloak_schema.Credentials(
                username=identity.username,
                user_id=identity.user_id
            )
        )

        minio_client = get_minio_client(
            identity=identity
        )

        if minio_client.bucket_exists(identity.username) == False:
            minio_client.make_bucket(
                bucket_name=identity.username
            )

            minio_client.set_bucket_versioning(
                bucket_name=identity.username,
                config=VersioningConfig(ENABLED)
            )

        minio_req = minio_client.put_object(
            bucket_name=identity.username,
            object_name="instance_" + str(edit_instance_req.id) + ".yaml",
            data=io.BytesIO(bytes(edited_yaml, 'utf-8')),
            length=len(edited_yaml),
            content_type="application/x-yaml"
        )

        update_release_response_data = platform_schema.UpdateReleaseResponseData(
            update_status=platform_schema.UpdateReleaseStatus(
                instance=platform_schema.UpdateReleaseInstanceStatus(
                    success=True,
                    message="Instance is updated in database."
                ),
                kubeapps=platform_schema.UpdateReleaseKubeappsStatus(
                    success=True,
                    message="Kubeapps release is updated."
                ),
                minio=platform_schema.UpdateReleaseMinioStatus(
                    success=True,
                    message="MinIO values are updated."
                ),
            )
        )

        return PlatformResponse(
            status_code=200,
            message="Instance is being edited",
            data=update_release_response_data.dict()
        )

    else: 

        update_release_response_data = platform_schema.UpdateReleaseResponseData(
            update_status=platform_schema.UpdateReleaseStatus(
                instance=platform_schema.UpdateReleaseInstanceStatus(
                    success=False,
                    message="Upper error."
                ),
                kubeapps=platform_schema.UpdateReleaseKubeappsStatus(
                    success=False,
                    message="Kubeapps release cannot be updated."
                ),
                minio=platform_schema.UpdateReleaseMinioStatus(
                    success=False,
                    message="Upper error."
                ),
            )
        )

        return PlatformResponse(
            status_code=406,
            message="Cannot update instance",
            data=update_release_response_data.dict()
        )

    
# replace it with smarter helm value picker !
def manipulate_values(helm_values: str, identity: keycloak_schema.Identity):
    received_yaml = yaml.safe_load(helm_values)
    received_yaml["namespace"] = identity.username
    converted_yaml = yaml.dump(received_yaml, allow_unicode=True)
    return converted_yaml


def generate_edited_yaml(
    json_values: dict, 
    instance: instance_schema.Instance, 
    db: Session
):
    
    instance_yaml = yaml.safe_load(instance.helm_values)
    for key in json_values:
        if key not in instance_yaml:
            return False, ""
        instance_yaml[key] = json_values[key]

    edited_yaml = yaml.dump(instance_yaml, allow_unicode=True)

    return True, edited_yaml


    