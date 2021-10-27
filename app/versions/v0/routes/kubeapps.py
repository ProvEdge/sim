
from fastapi import Depends, APIRouter

from database.schemas import keycloak_schema, kubeapps_schema

from app.functions import kubeapps_rest_crud
from app.functions.general_functions import generate_response, match_identity

router = APIRouter()

@router.get("/releases")
def get_releases(
    identity: keycloak_schema.Identity = Depends(match_identity)
):
    try:
        get_releases_req = kubeapps_rest_crud.get_releases(
            id_token=identity.id_token
        )

        if get_releases_req.status_code == 200:
            return generate_response(
                "SUCCESS", 
                "Releases are returned", 
                get_releases_req.data
            )

        return generate_response(
            "FAILURE", 
            "Cannot get releases",
            get_releases_req.data
        )

    except Exception as e:
        return generate_response(
            status="FAILURE", 
            message=str(e)
        )


@router.get("/releases/{namespace}")
def get_releases_by_namespaces(
    namespace: str,
    identity: keycloak_schema.Identity = Depends(match_identity)
):
    try:
        get_releases_req = kubeapps_rest_crud.get_releases_by_namespace(
            id_token=identity.id_token,
            namespace=namespace
        )

        if get_releases_req.status_code == 200:
            return generate_response(
                "SUCCESS", 
                "Releases are returned", 
                get_releases_req.data
            )

        return generate_response(
            "FAILURE", 
            "Cannot get releases",
            get_releases_req.data
        )

    except Exception as e:
        return generate_response(
            status="FAILURE", 
            message=str(e)
        )


@router.get("/releases/{namespace}/{release}")
def get_release(
    namespace: str,
    release: str,
    identity: keycloak_schema.Identity = Depends(match_identity)
):
    try:
        get_release_req = kubeapps_rest_crud.get_release(
            id_token=identity.id_token,
            namespace=namespace,
            release=release
        )

        if get_release_req.status_code == 200:
            return generate_response(
                "SUCCESS", 
                "Release is returned", 
                get_release_req.data
            )

        return generate_response(
            "FAILURE", 
            "Cannot get release",
            get_release_req.data
        )
        
    except Exception as e:
        return generate_response(
            status="FAILURE", 
            message=str(e)
        )



@router.post("/releases/{namespace}")
def create_release(
    namespace: str,
    release: kubeapps_schema.CreateRelease,
    identity: keycloak_schema.Identity = Depends(match_identity)
):
    try:
        create_release_req = kubeapps_rest_crud.post_release(
            id_token=identity.id_token,
            namespace=namespace,
            release=release
        )
        return generate_response(
            "SUCCESS", 
            "Release is created", 
            create_release_req.data
        )
    except Exception as e:
        return generate_response(
            status="FAILURE", 
            message=str(e)
        )


@router.delete("/releases/{namespace}/{release}")
def delete_release(
    namespace: str,
    release: str,
    identity: keycloak_schema.Identity = Depends(match_identity)
):
    try:
        releases = kubeapps_rest_crud.delete_release(
            id_token=identity.id_token,
            namespace=namespace,
            release=release
        )

        print(releases.status_code)

        return generate_response(
            "SUCCESS", 
            "Release is deleted", 
            releases.data
        )
    except Exception as e:
        return generate_response(
            status="FAILURE", 
            message=str(e)
        )