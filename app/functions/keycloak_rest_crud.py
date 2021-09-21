from app.versions.v0.routes.users import EditUser
import requests

import json



keycloak_server_url = "https://keycloaktest.provedge.cloud/auth/admin/realms"

def get_users(admin_access_token: str):
    
    route =   "/kubernetes-platform/users"
    url = keycloak_server_url + route
    auth_header = {
        "Authorization": "Bearer " + admin_access_token
    }

    response = requests.get(url=url, headers=auth_header)
    response_json = {"users": response.json()}
    return response_json

def get_user(admin_access_token: str, id: str):
    
    route = "/kubernetes-platform/users/" + id
    url = keycloak_server_url + route
    auth_header = {
        "Authorization": "Bearer " + admin_access_token
    }

    response = requests.get(url=url, headers=auth_header)
    response_json = {"user": response.json()}
    return response_json

def edit_user(admin_access_token: str, id: str, data: EditUser):

    route = "/kubernetes-platform/users/" + id
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
    
    return_message = response.json

    if response.status_code == 204:
        return_message = {
            "user": "Update is successful"
        }

    return return_message

def delete_user(admin_access_token: str, id: str):
    
    route = "/kubernetes-platform/users/" + id
    url = keycloak_server_url + route

    auth_header = {
        "Authorization": "Bearer " + admin_access_token,
    }

    response = requests.delete(url=url, headers=auth_header)

    return_message = response.json

    if response.status_code == 204:
        return_message = {
            "user": "Delete is successful"
        }
    
    return return_message

def get_users_groups(admin_access_token: str, id: str):
    
    route = "/kubernetes-platform/users/" + id + "/groups"
    url = keycloak_server_url + route
    auth_header = {
        "Authorization": "Bearer " + admin_access_token
    }

    response = requests.get(url=url, headers=auth_header)
    response_json = {"groups": response.json()}
    return response_json
    

def get_groups(admin_access_token: str):
    
    route = "/kubernetes-platform/groups"
    url = keycloak_server_url + route
    auth_header = {
        "Authorization": "Bearer " + admin_access_token
    }

    response = requests.get(url=url, headers=auth_header)
    return response.json()


def get_group(admin_access_token: str, id: str):
    
    route = "/kubernetes-platform/groups/" + id
    url = keycloak_server_url + route
    auth_header = {
        "Authorization": "Bearer " + admin_access_token
    }

    response = requests.get(url=url, headers=auth_header)
    return response.json()