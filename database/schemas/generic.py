from typing import List, Optional, Union

from fastapi_camelcase import CamelModel

class ResponseBase(CamelModel):
    status: str
    message: str
    data: dict