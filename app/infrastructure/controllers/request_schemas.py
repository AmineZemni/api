from pydantic import BaseModel
from fastapi import UploadFile


class CalculationSampleRequest(BaseModel):
    value1: float
    value2: float


class CalculationLKDRequest(BaseModel):
    aoc_step_file: UploadFile
    calc_process_file: UploadFile
    cf_items_file: UploadFile
    discount_types_file: UploadFile
    reporting_process_file: UploadFile
    run_types_file: UploadFile
    timeframe_file: UploadFile
    uao_file: UploadFile
    lrc_input_proj_file: UploadFile
    monthly_yield_curves_file: UploadFile
