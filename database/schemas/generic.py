from typing import List, Optional, Union

from pydantic import BaseModel

class ResponseBase(BaseModel):
    status: str
    message: str
    data: dict