from typing import List, Optional
from fastapi_camelcase import CamelModel

from .generic import ResponseBase

class BillBase(CamelModel):
    usage_id: int
    amount: float
    currency: str = "USD"
    is_paid: bool = False

class BillCreate(BillBase):
    pass

class BillEdit(CamelModel):
    is_paid: bool

class Bill(BillBase):
    id: int
    class Config:
        orm_mode = True

class ListBillsResponse(ResponseBase):
    data: List[Bill]

class GetBillResponse(ResponseBase):
    data: Bill

