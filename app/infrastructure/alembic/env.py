import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from app.infrastructure.models.base import Base  # Corrected import for Base

# Load Alembic configuration
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get the database URL from environment (Ensure .env is loaded before this)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment")

# Convert asyncpg URL to psycopg2 for Alembic migrations
SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")

config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

# Create a synchronous engine for migrations
engine = create_engine(SYNC_DATABASE_URL, poolclass=pool.NullPool)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=SYNC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},  # Ensure compatibility
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            dialect_opts={"paramstyle": "named"},  # Ensure compatibility
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
