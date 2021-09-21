import requests

from database.schemas import keycloak_schema

def get_admin_credentials() -> keycloak_schema.AdminAccessCredentials:
    url = "https://keycloaktest.provedge.cloud/auth/realms/master/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": "admin",
        "password": "admin",
        "realm": "master",
        "scope": "openid"
    }
    response = requests.post(url=url, data=data)

    json_response = response.json()
    
    return json_response