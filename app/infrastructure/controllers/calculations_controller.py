from app.infrastructure.controllers.request_schemas import (
    CalculationLKDRequest,
    CalculationSampleRequest,
)
from app.infrastructure.controllers.response_schemas import (
    CalculationSampleResponse,
    CalculationIdResponse,
)
from app.application.commands.add_values_command_handler import addValuesCommandHandler
from app.application.commands.calculate_lkd_bloc_command_handler import (
    calculateLKDBlocCommandHandler,
)

from fastapi import APIRouter, UploadFile, File, HTTPException

calculations_router = APIRouter()


@calculations_router.post("/sample", response_model=CalculationSampleResponse)
def postCalculation(calculation: CalculationSampleRequest):
    result = addValuesCommandHandler.execute(calculation)
    return CalculationSampleResponse(result=result)


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

    calculation_files = CalculationLKDRequest(
        aoc_step_file=aoc_step_file,
        calc_process_file=calc_process_file,
        cf_items_file=cf_items_file,
        discount_types_file=discount_types_file,
        reporting_process_file=reporting_process_file,
        run_types_file=run_types_file,
        timeframe_file=timeframe_file,
        uao_file=uao_file,
        lrc_input_proj_file=lrc_input_proj_file,
        monthly_yield_curves_file=monthly_yield_curves_file,
    )

    calculation_id = await calculateLKDBlocCommandHandler.execute(calculation_files)
    return CalculationIdResponse(id=calculation_id)
