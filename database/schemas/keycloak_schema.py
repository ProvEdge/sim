from pydantic import BaseModel

class AdminAccessCredentials(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str