import os
from fastapi import FastAPI
from app.controllers.calculations_controller import calculations_router
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database

# Load env vars
load_dotenv()


@asynccontextmanager
async def lifespan():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in the environment")

    SYNC_DATABASE_URL = DATABASE_URL.replace(
        "postgresql+asyncpg", "postgresql+psycopg2"
    )
    if not database_exists(SYNC_DATABASE_URL):
        create_database(SYNC_DATABASE_URL)
        print(f"✅ Database created: {SYNC_DATABASE_URL}")
    else:
        print("✅ Database already exists.")

    yield  # Startup continues


app = FastAPI(
    lifespan=lifespan,
    title="IFRS17 API",
    description="IFRS17 API",
    version="1.0.0",
)


@app.get("/", summary="Root Endpoint", description="Returns a welcome message.")
def read_root():
    return {"message": "Hello, FastAPI!"}


app.include_router(calculations_router)
