from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

class BillBase(BaseModel):
    usage_id: int
    amount: float
    currency: str
    is_paid: bool = False

class BillCreate(BillBase):
    pass

class BillEdit(BaseModel):
    is_paid: bool

class Bill(BillBase):
    id: int
    class Config:
        orm_mode = True

class ListBillsResponse(ResponseBase):
    data: List[Bill]

class GetBillResponse(ResponseBase):
    data: Bill

