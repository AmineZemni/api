from fastapi import APIRouter, Form
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict
from pathlib import Path
import uuid
import datetime
import yaml
from app.infrastructure.alembic.models.form_run_settings_model import (
    FormInputRunSettings,
    FormRunSettings,
)


# Create router
form_router = APIRouter(
    prefix="/form-run-settings",
    tags=["Form Run Settings"],
    responses={404: {"description": "Not found"}},
)

# In-memory storage (replace with database in production)
form_storage = {}


@form_router.post(
    "/",
    response_model=FormInputRunSettings,
    status_code=status.HTTP_201_CREATED,
    summary="Submit form run settings",
    description="Submit form run settings with automatic ID generation",
)
async def submit_form(
    start_date: str = Form(...),
    projection_periods: int = Form(...),
    valuation_date: str = Form(...),
    cancellation_penalty_rate: float = Form(...),
    fees_for_malath_being_leader: float = Form(...),
    malath_share_of_pool: float = Form(...),
    malath_lead_limit_date: str = Form(...),
    first_management_expense_pc: float = Form(...),
    deposit_premium_rate: float = Form(...),
    activation_premium_rate: float = Form(...),
    reinsurance_commissions_amortisation: float = Form(...),
    reporting_date: str = Form(...),
    next_reporting_date: str = Form(...),
    chunk_size: int = Form(...),
    run_policies: str = Form(...),
    run_model: str = Form(...),
    nonactivated_policy_nonproj_results: str = Form(...),
    path_nonactivated_policy_nonproj_results: str = Form(...),
    activated_policy_nonproj_results: str = Form(...),
    path_activated_policy_nonproj_results: str = Form(...),
    nonactivated_policy_monthproj_results: str = Form(...),
    path_nonactivated_policy_monthproj_results: str = Form(...),
    activated_policy_monthproj_results: str = Form(...),
    path_activated_policy_monthproj_results: str = Form(...),
    cohort_quarterproj_results: str = Form(...),
    policies_sample: str = Form(...),  # Accept as a comma-separated string
):

    # Convert `policies_sample` from a comma-separated string to a list of integers
    try:
        policies_sample_list = [int(x.strip()) for x in policies_sample.split(",")]
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid policies_sample format. Expected comma-separated integers.",
        )

    run_settings = FormRunSettings(
        start_date=start_date,
        projection_periods=projection_periods,
        valuation_date=valuation_date,
        cancellation_penalty_rate=cancellation_penalty_rate,
        fees_for_malath_being_leader=fees_for_malath_being_leader,
        malath_share_of_pool=malath_share_of_pool,
        malath_lead_limit_date=malath_lead_limit_date,
        first_management_expense_pc=first_management_expense_pc,
        deposit_premium_rate=deposit_premium_rate,
        activation_premium_rate=activation_premium_rate,
        reinsurance_commissions_amortisation=reinsurance_commissions_amortisation,
        reporting_date=reporting_date,
        next_reporting_date=next_reporting_date,
        chunk_size=chunk_size,
        run_policies=run_policies,
        run_model=run_model,
        nonactivated_policy_nonproj_results=nonactivated_policy_nonproj_results,
        path_nonactivated_policy_nonproj_results=path_nonactivated_policy_nonproj_results,
        activated_policy_nonproj_results=activated_policy_nonproj_results,
        path_activated_policy_nonproj_results=path_activated_policy_nonproj_results,
        nonactivated_policy_monthproj_results=nonactivated_policy_monthproj_results,
        path_nonactivated_policy_monthproj_results=path_nonactivated_policy_monthproj_results,
        activated_policy_monthproj_results=activated_policy_monthproj_results,
        path_activated_policy_monthproj_results=path_activated_policy_monthproj_results,
        cohort_quarterproj_results=cohort_quarterproj_results,
        policies_sample=policies_sample_list,
    )

    form_input = FormInputRunSettings(run_settings=run_settings)
    form_storage[form_input.id] = form_input.model_dump()  # Store validated form data

    yaml_file_path = Path("app/infrastructure/alembic/run_settings/form_run_settings")
    yaml_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(yaml_file_path, "w") as yaml_file:
        yaml.dump(form_storage, yaml_file, default_flow_style=False, allow_unicode=True)

    print(f"✅ YAML file saved at: {yaml_file_path}")

    return form_input


@form_router.get(
    "/{form_id}",
    response_model=FormInputRunSettings,
    summary="Get form run settings by ID",
    responses={
        404: {"description": "Form settings not found"},
        200: {
            "description": "Form settings retrieved successfully",
        },
    },
)
async def get_form(form_id: str):

    if form_id not in form_storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Form settings not found"
        )
    return form_storage[form_id]


@form_router.get(
    "/", response_model=List[FormInputRunSettings], summary="List all form run settings"
)
async def list_forms():

    return list(form_storage.values())


@form_router.delete(
    "/{form_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete form run settings",
)
async def delete_form(form_id: str):

    if form_id not in form_storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Form settings not found"
        )
    del form_storage[form_id]
    return None
