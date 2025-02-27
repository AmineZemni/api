from app.infrastructure.controllers.schemas import (
    CalculationRequest,
    CalculationResponse,
)
from app.application.commands.add_values_command_handler import addValuesCommandHandler
from fastapi import APIRouter

calculations_router = APIRouter()


@calculations_router.post("/sample", response_model=CalculationResponse)
def postCalculation(calculation: CalculationRequest):
    result = addValuesCommandHandler.execute(calculation.value1, calculation.value2)
    return CalculationResponse(result=result)
