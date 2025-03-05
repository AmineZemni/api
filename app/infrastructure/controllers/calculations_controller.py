from app.infrastructure.controllers.schemas import (
    CalculationIdResponse,
    CalculationSampleRequest,
    CalculationSampleResponse,
)
from app.application.commands.add_values_command_handler import addValuesCommandHandler
from app.application.commands.calculate_lkd_bloc_command_handler import (
    calculateLKDBlocCommandHandler,
)

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

calculations_router = APIRouter()


@calculations_router.post("/sample", response_model=CalculationSampleResponse)
def postCalculation(calculation: CalculationSampleRequest):
    result = addValuesCommandHandler.execute(calculation.value1, calculation.value2)
    return CalculationSampleResponse(result=result)


'''
@calculations_router.post("/lkd-bloc", response_model=CalculationIdResponse)
def postCalculation():
    """Endpoint for LKD bloc calculation (legacy version)."""
    id = calculateLKDBlocCommandHandler.execute()
    return CalculationIdResponse(id=id)
'''


@calculations_router.post("/lkd-bloc", response_model=CalculationIdResponse)
async def calculate_lkd(
    aoc_step_file: UploadFile = File(...),
    calc_process_file: UploadFile = File(...),
    cf_items_file: UploadFile = File(...),
    discount_types_file: UploadFile = File(...),
    reporting_process_file: UploadFile = File(...),
    run_types_file: UploadFile = File(...),
    timeframe_file: UploadFile = File(...),
    uao_file: UploadFile = File(...),
    lrc_input_proj_file: UploadFile = File(...),
    monthly_yield_curves_file: UploadFile = File(...),
):
    """Endpoint to calculate LKD using uploaded CSV files."""
    try:
        handler = calculateLKDBlocCommandHandler
        calculation_id = await handler.execute(
            aoc_step_file,
            calc_process_file,
            cf_items_file,
            discount_types_file,
            reporting_process_file,
            run_types_file,
            timeframe_file,
            uao_file,
            lrc_input_proj_file,
            monthly_yield_curves_file,
        )
        return CalculationIdResponse(id=calculation_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
