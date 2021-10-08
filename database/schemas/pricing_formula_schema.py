from typing import List, Optional
from pydantic import BaseModel

from .generic import ResponseBase

class PricingFormulaBase(BaseModel):
    name: str
    robot_type: str = "jackal"
    robot_coefficient: float
    time_unit: str = "minute"
    amount_per_time_unit: float
    currency: str = "USD"

class PricingFormulaCreate(PricingFormulaBase):
    pass

class PricingFormulaEdit(BaseModel):
    name: Optional[str]
    robot_type: Optional[str]
    robot_coefficient: Optional[float]
    time_unit: Optional[str]
    amount_per_time_unit: Optional[float]
    currency: Optional[str]

class PricingFormula(PricingFormulaBase):
    class Config:
        orm_mode = True

class ListPricingFormulasResponse(ResponseBase):
    data: List[PricingFormula]

class GetPricingFormulaResponse(ResponseBase):
    data: PricingFormula

