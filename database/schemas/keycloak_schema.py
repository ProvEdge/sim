from fastapi_camelcase import CamelModel

class AdminAccessCredentials(CamelModel):
    access_token: str
    refresh_token: str
    id_token: str

class KCResponse():
    def __init__(self, status_code: int, data: dict):
        self.status_code = status_code
        self.data = data

class Credentials(CamelModel):
    user_id: str
    username: str

class Identity(Credentials):
    id_token: str
