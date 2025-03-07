from fastapi import Form
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid


class FormRunSettings(BaseModel):
    start_date: str
    projection_periods: int
    valuation_date: str
    cancellation_penalty_rate: float
    fees_for_malath_being_leader: float
    malath_share_of_pool: float
    malath_lead_limit_date: str
    first_management_expense_pc: float
    deposit_premium_rate: float
    activation_premium_rate: float
    reinsurance_commissions_amortisation: float
    reporting_date: str
    next_reporting_date: str
    chunk_size: int
    run_policies: str
    run_model: str
    nonactivated_policy_nonproj_results: str
    path_nonactivated_policy_nonproj_results: str
    activated_policy_nonproj_results: str
    path_activated_policy_nonproj_results: str
    nonactivated_policy_monthproj_results: str
    path_nonactivated_policy_monthproj_results: str
    activated_policy_monthproj_results: str
    path_activated_policy_monthproj_results: str
    cohort_quarterproj_results: str
    policies_sample: List[int]


class FormInputRunSettings(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    run_settings: FormRunSettings


"""
What's Wrong with instantiatin like this FormInputRunSettings = FormInputRunSettings()

You're creating an instance of FormInputRunSettings without passing required fields.

Pydantic expects all required fields to be present unless they have default values.

"""
form_input_run_settings = FormInputRunSettings(
    run_settings=FormRunSettings(
        start_date="31/12/2020",
        projection_periods=500,
        valuation_date="31/12/2024",
        cancellation_penalty_rate=0.0,
        fees_for_malath_being_leader=0.0,
        malath_share_of_pool=1.0,
        malath_lead_limit_date="24/06/2065",
        first_management_expense_pc=0.9,
        deposit_premium_rate=0.3,
        activation_premium_rate=0.7,
        reinsurance_commissions_amortisation=0.025,
        reporting_date="31/12/2024",
        next_reporting_date="31/03/2025",
        chunk_size=1000,
        run_policies="all_policies",
        run_model="after_activation",
        nonactivated_policy_nonproj_results="N",
        path_nonactivated_policy_nonproj_results="local_runs/run_exports/nonactivated_policy_nonproj_results.csv",
        activated_policy_nonproj_results="N",
        path_activated_policy_nonproj_results="local_runs/run_exports/activated_policy_nonproj_results.csv",
        nonactivated_policy_monthproj_results="N",
        path_nonactivated_policy_monthproj_results="local_runs/run_exports/nonactivated_policy_monthproj_results.csv",
        activated_policy_monthproj_results="N",
        path_activated_policy_monthproj_results="local_runs/run_exports/activated_policy_monthproj_results.csv",
        cohort_quarterproj_results="Y",
        policies_sample=[25043197, 25029044],
    )
)

# test to verify the object is created correctly
print(form_input_run_settings)
