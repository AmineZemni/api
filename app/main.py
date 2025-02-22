from fastapi import FastAPI
from app.controllers.calculations_controller import calculations_router

app = FastAPI(
    title="Calculations API",
    description="A simple API that adds two numbers.",
    version="1.0.0",
)

app.include_router(calculations_router, prefix="/calculations")


@app.get("/")
def read_root():
    return {"message": "Hello, STAGEEEEEEEE 2025      !"}
