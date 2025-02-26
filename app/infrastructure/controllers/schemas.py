# app/controllers/schemas.py
from pydantic import BaseModel
from uuid import UUID


class CalculationRequest(BaseModel):
    x1: float
    x2: float


class CalculationResponse(BaseModel):
    id: UUID
    x1: float
    x2: float
    sum: float

    class Config:
        orm_mode = True
