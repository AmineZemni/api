from app.infrastructure.controllers.calculations_controller import calculations_router
from app.app import app


@app.get("/", summary="Root Endpoint", description="Returns a welcome message.")
def read_root():
    return {"message": "Hello, FastAPI!"}


app.include_router(calculations_router)
