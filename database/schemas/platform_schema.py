from pydantic import BaseModel

class PlatformResponse(BaseModel):
    status_code: str
    message: str
    data: dict

class CreateInstance(BaseModel):
    name: str
    robot_type: str