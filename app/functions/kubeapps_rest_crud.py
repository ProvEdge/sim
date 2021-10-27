from database.schemas import kubeapps_schema
import requests, json

from database.schemas.kubeapps_schema import KubeappsResponse

kubeapps_server_url = "http://23.88.62.179:32510/api"

def get_releases(id_token: str) -> KubeappsResponse:
    
    route = "/kubeops/v1/clusters/default/releases"
    url = kubeapps_server_url + route

    response = requests.get(
        url=url, 
        headers=prepare_auth_header(id_token)
    )
    status_code = response.status_code
    data = response.json()

    return KubeappsResponse(
        status_code=status_code,
        data=data
    )
    

def get_releases_by_namespace(
    id_token: str, 
    namespace: str
) -> KubeappsResponse:
    
    route = "/kubeops/v1/clusters/default/namespaces/" + namespace + "/releases"
    url = kubeapps_server_url + route

    response = requests.get(
        url=url, 
        headers=prepare_auth_header(id_token)
    )
    status_code = response.status_code
    data = response.json()

    return KubeappsResponse(
        status_code=status_code,
        data=data
    )


def get_release(
    id_token: str, 
    namespace: str,
    release: str
) -> KubeappsResponse:
    
    route = "/kubeops/v1/clusters/default/namespaces/" + namespace + "/releases/" + release
    url = kubeapps_server_url + route

    response = requests.get(
        url=url, 
        headers=prepare_auth_header(id_token)
    )
    status_code = response.status_code
    data = response.json()

    return KubeappsResponse(
        status_code=status_code,
        data=data
    )


def post_release(
    id_token: str,
    namespace: str,
    release: kubeapps_schema.CreateRelease
) -> KubeappsResponse:
    
    route = "/kubeops/v1/clusters/default/namespaces/" + namespace + "/releases"
    url = kubeapps_server_url + route

    response = requests.post(
        url=url, 
        headers=prepare_auth_header(id_token),
        json=release.dict()
    )

    status_code = response.status_code
    data = response.json()

    return KubeappsResponse(
        status_code=status_code,
        data=data
    )


def delete_release(
    id_token: str, 
    namespace: str,
    release: str
) -> KubeappsResponse:
    
    route = "/kubeops/v1/clusters/default/namespaces/" + namespace + "/releases/" + release
    url = kubeapps_server_url + route

    response = requests.delete(
        url=url, 
        headers=prepare_auth_header(id_token)
    )
    status_code = response.status_code
    data = response.json()

    return KubeappsResponse(
        status_code=status_code,
        data=data
    )
    

def update_release(
    id_token: str, 
    namespace: str,
    release_name: str,
    release: kubeapps_schema.UpdateRelease
) -> KubeappsResponse:
    
    route = "/kubeops/v1/clusters/default/namespaces/" + namespace + "/releases/" + release_name
    url = kubeapps_server_url + route

    release_dict = release.dict()
    release_proper_dict = {k: v for k, v in release_dict.items() if v is not None}

    response = requests.put(
        url=url, 
        headers=prepare_auth_header(id_token),
        json=release_proper_dict
    )

    status_code = response.status_code
    data = response.json()

    return KubeappsResponse(
        status_code=status_code,
        data=data
    )


def prepare_auth_header(id_token: str):
    return {
        "Authorization": "Bearer " + id_token
    }