# app/controllers/calculations_controller.py
import sqlalchemy as sa
from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.controllers.schemas import CalculationRequest, CalculationResponse
from app.controllers.models import Calculation
from app.application.commands.add_values_command_handler import addValuesCommandHandler
from app.infrastructure.models.base import async_session


calculations_router = APIRouter(
    prefix="/calculations",
    tags=["Calculations"],
    responses={404: {"description": "Not found"}},
)


# POST /calculations: Create a new calculation and persist it in the database.
@calculations_router.post(
    "",
    response_model=CalculationResponse,
    summary="Create Calculation",
    description="Calculates the result and saves it to the database.",
)
async def post_calculation(calculation: CalculationRequest):
    try:
        # The command handler will create and persist the Calculation instance.
        record = await addValuesCommandHandler.execute(calculation.x1, calculation.x2)
        # Assuming your Pydantic response schema can be created from the ORM model,
        # return the record directly.
        return record
    except Exception as e:
        # In a real application, log the exception details.
        raise HTTPException(status_code=500, detail="Internal Server Error")


# GET /calculations/{uid}: Retrieve a calculation result by its UID.
# @calculations_router.get(
#     "/{uid}",
#     response_model=CalculationResponse,
#     summary="Retrieve Calculation",
#     description="Retrieves a calculation by its UID."
# )
# async def get_calculation(uid: str):
#     # Validate that the provided uid is a valid UUID.
#     try:
#         uid_obj = UUID(uid)
#     except ValueError:
#         raise HTTPException(status_code=422, detail="Invalid UID format")

#     async with async_session() as session:
#         # Use session.get() to load the Calculation by primary key (id).
#         record = await session.get(Calculation, uid_obj)
#         if not record:
#             raise HTTPException(status_code=404, detail="Calculation not found")
#         return record
