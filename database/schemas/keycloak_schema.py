from pydantic import BaseModel

class AdminAccessCredentials(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str

class KCResponse():
    def __init__(self, status_code: int, data: dict):
        self.status_code = status_code
        self.data = data