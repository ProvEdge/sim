from fastapi import params
from database.schemas import group_schema, user_schema
import requests, json

from database.schemas.keycloak_schema import KCResponse

realm = "master"

keycloak_server_url = "https://keycloaktest.provedge.cloud/auth/admin/realms/" + realm

def get_users(admin_access_token: str) -> KCResponse:
    
    route = "/users"
    url = keycloak_server_url + route
    auth_header = {
        "Authorization": "Bearer " + admin_access_token
    }

    response = requests.get(url=url, headers=auth_header)
    status_code = response.status_code
    data = response.json()

    return KCResponse(
        status_code=status_code,
        data=data
    )

def get_user(admin_access_token: str, id: str) -> KCResponse:
    
    route = "/users/" + id
    url = keycloak_server_url + route
    auth_header = {
        "Authorization": "Bearer " + admin_access_token
    }

    response = requests.get(url=url, headers=auth_header)
    status_code = response.status_code
    data = response.json()

    return KCResponse(
        status_code=status_code,
        data=data
    )

def edit_user(admin_access_token: str, id: str, data: user_schema.EditUserRequest) -> KCResponse:

    route = "/users/" + id
    url = keycloak_server_url + route

    auth_header = {
        "Authorization": "Bearer " + admin_access_token,
        "Content-Type": "application/json",
        "Accept": "*/*"
    }

    user_rep = {}

    for attr, value in data.__dict__.items():
        if value is not None:
            user_rep[attr] = value


    response = requests.put(url=url, headers=auth_header, data=json.dumps(user_rep))
    status_code = response.status_code

    if status_code == 204: data = get_user(admin_access_token, id).data
    else: data = {}

    return KCResponse(
        status_code=status_code,
        data=data
    )

def get_user_attributes(admin_access_token: str, id: str) -> KCResponse:
    
    user_req = get_user(admin_access_token, id)
    if user_req.status_code == 404:
        return user_req

    if "attributes" not in user_req.data: return KCResponse(
        status_code=200,
        data={}
    )
    else: return KCResponse(
        status_code=200,
        data=user_req.data["attributes"]
    )

def add_user_attributes(admin_access_token: str, id: str, data: user_schema.AddAttributesRequest) -> KCResponse:
    
    user_req = get_user(admin_access_token, id)
    if user_req.status_code == 404:
        return user_req
    
    cur_attr = get_user_attributes(admin_access_token, id).data
    data.attributes = {**cur_attr, **data.attributes}

    edit_req = edit_user(admin_access_token, id, data=data)

    return edit_req


def delete_user(admin_access_token: str, id: str) -> KCResponse:
    
    user_req = get_user(admin_access_token, id)
    if user_req.status_code == 404:
        return user_req

    route = "/users/" + id
    url = keycloak_server_url + route

    auth_header = {
        "Authorization": "Bearer " + admin_access_token,
    }

    response = requests.delete(url=url, headers=auth_header)
    status_code = response.status_code
    data = {}

    if status_code == 204:
        data = user_req.data
    
    return KCResponse(
        status_code=status_code,
        data=data
    )

def get_users_groups(admin_access_token: str, id: str) -> KCResponse:

    user_req = get_user(admin_access_token, id)
    if user_req.status_code == 404:
        return user_req
    
    route = "/users/" + id + "/groups"
    url = keycloak_server_url + route
    auth_header = {
        "Authorization": "Bearer " + admin_access_token
    }

    response = requests.get(url=url, headers=auth_header)
    status_code = response.status_code
    data = response.json()

    return KCResponse(
        status_code=status_code,
        data=data
    )
    

def get_groups(admin_access_token: str, brief: bool) -> KCResponse:
    
    route = "/groups"
    url = keycloak_server_url + route
    auth_header = {
        "Authorization": "Bearer " + admin_access_token
    }

    parameters = {
        "briefRepresentation": brief
    }

    response = requests.get(url=url, headers=auth_header, params=parameters)
    status_code = response.status_code
    data = response.json()

    return KCResponse(
        status_code=status_code,
        data=data
    )


def get_group(admin_access_token: str, id: str) -> KCResponse:
    
    route = "/groups/" + id
    url = keycloak_server_url + route
    auth_header = {
        "Authorization": "Bearer " + admin_access_token
    }

    response = requests.get(url=url, headers=auth_header)
    status_code = response.status_code
    data = response.json()

    return KCResponse(
        status_code=status_code,
        data=data
    )

def get_group_members(admin_access_token: str, id: str) -> KCResponse:
    
    route = "/groups/" + id + "/members"
    url = keycloak_server_url + route
    auth_header = {
        "Authorization": "Bearer " + admin_access_token
    }

    response = requests.get(url=url, headers=auth_header)
    status_code = response.status_code
    data = response.json()

    return KCResponse(
        status_code=status_code,
        data=data
    )


def edit_group(admin_access_token: str, id: str, data: group_schema.EditGroupRequest) -> KCResponse:

    route = "/groups/" + id
    url = keycloak_server_url + route

    auth_header = {
        "Authorization": "Bearer " + admin_access_token,
        "Content-Type": "application/json",
        "Accept": "*/*"
    }

    group_rep = {}

    for attr, value in data.__dict__.items():
        if value is not None:
            group_rep[attr] = value

    print(group_rep)

    response = requests.put(url=url, headers=auth_header, data=json.dumps(group_rep))
    status_code = response.status_code

    if status_code == 204: data = get_group(admin_access_token, id).data
    else: data = {}

    return KCResponse(
        status_code=status_code,
        data=data
    )



def delete_group(admin_access_token: str, id: str) -> KCResponse:
    
    group_req = get_group(admin_access_token, id)
    if group_req.status_code == 404:
        return group_req

    route = "/groups/" + id
    url = keycloak_server_url + route

    auth_header = {
        "Authorization": "Bearer " + admin_access_token,
    }

    response = requests.delete(url=url, headers=auth_header)
    status_code = response.status_code
    data = {}

    if status_code == 204:
        data = group_req.data
    
    return KCResponse(
        status_code=status_code,
        data=data
    )


def get_group_attributes(admin_access_token: str, id: str) -> KCResponse:
    
    group_req = get_group(admin_access_token, id)
    if group_req.status_code == 404:
        return group_req

    if "attributes" not in group_req.data: return KCResponse(
        status_code=200,
        data={}
    )
    else: return KCResponse(
        status_code=200,
        data=group_req.data["attributes"]
    )


def add_group_attributes(admin_access_token: str, id: str, data: group_schema.AddAttributesRequest) -> KCResponse:
    
    group_req = get_group(admin_access_token, id)
    if group_req.status_code == 404:
        return group_req
    
    cur_attr = get_group_attributes(admin_access_token, id).data
    data.attributes = {**cur_attr, **data.attributes}

    edit_req = edit_group(admin_access_token, id, data=data)
    status_code = edit_req.status_code
    res_data = {}
    if status_code == 204: res_data = get_group_attributes(admin_access_token, id).data
    else: res_data = {}

    return KCResponse(
        status_code=status_code,
        data=res_data
    )
