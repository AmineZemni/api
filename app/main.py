from fastapi import FastAPI, Depends
from app.database import DatabaseService
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.infrastructure.controllers.calculations_controller import calculations_router
from app.infrastructure.controllers.form_run_settings_controller import form_router

db_service = DatabaseService()

app = FastAPI(
    title="Novacture API",
    description="Novacture API",
    version="1.0.0",
)


@app.get("/", summary="Health Endpoint", description="Returns ok.")
def hello():
    return {"status": "ok"}


@app.get("/db", summary="DB Health Endpoint", description="Returns ok if db is ok.")
def db(session: Session = Depends(db_service.get_session)):
    result = session.execute(text("SELECT 1"))
    return {"message": "hello", "db_status": result.scalar_one()}


app.include_router(calculations_router)
app.include_router(form_router)
