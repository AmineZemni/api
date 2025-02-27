import os

from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database
from contextlib import asynccontextmanager

# Load env vars
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: U100
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
