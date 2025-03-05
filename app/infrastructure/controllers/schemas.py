from pydantic import BaseModel


class CalculationSampleRequest(BaseModel):
    value1: float
    value2: float


class CalculationSampleResponse(BaseModel):
    result: float


class CalculationIdResponse(BaseModel):
    id: str
