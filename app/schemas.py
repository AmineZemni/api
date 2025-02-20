# Pydantic models for request/response
from pydantic import BaseModel

class CalculationRequest(BaseModel):
    value1: float
    value2: float

class CalculationResponse(BaseModel):
    result: float
