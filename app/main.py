# FastAPI entry point with API routes

from fastapi import FastAPI

app = FastAPI(
    title="Calculations API",
    description="A simple API that adds two numbers.",
    version="1.0.0"
)



# Hello World API

@app.get("/")
def read_root():
    return {"message": "Hello, STAGEEEEEEEE 2025      !"}


# Basic Calculations API with no Databse Integration

from app.schemas import CalculationRequest, CalculationResponse
from app.services import add_values

@app.post("/calculations/sample", response_model=CalculationResponse)

def calculate_sample(calculation: CalculationRequest):
    result = add_values(calculation.value1, calculation.value2)
    return CalculationResponse(result=result)
