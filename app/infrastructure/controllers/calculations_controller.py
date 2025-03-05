from app.infrastructure.controllers.schemas import (
    CalculationIdResponse,
    CalculationSampleRequest,
    CalculationSampleResponse,
)
from app.application.commands.add_values_command_handler import addValuesCommandHandler
from app.application.commands.calculate_lkd_bloc_command_handler import (
    calculateLKDBlocCommandHandler,
)
from fastapi import APIRouter

calculations_router = APIRouter()


@calculations_router.post("/sample", response_model=CalculationSampleResponse)
def postCalculation(calculation: CalculationSampleRequest):
    result = addValuesCommandHandler.execute(calculation.value1, calculation.value2)
    return CalculationSampleResponse(result=result)


@calculations_router.post("/lkd-bloc", response_model=CalculationIdResponse)
def postCalculation():
    id = calculateLKDBlocCommandHandler.execute()
    return CalculationIdResponse(id=id)
