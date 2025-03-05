from pydantic import BaseModel


class CalculationSampleResponse(BaseModel):
    result: float


class CalculationIdResponse(BaseModel):
    id: str
