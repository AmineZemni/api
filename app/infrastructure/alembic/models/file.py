from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.alembic.models.base import Base
import uuid
import sqlalchemy as sa


class FileMetadata(Base):
    __tablename__ = "file"

    id = Column(String, primary_key=True, default=str(uuid.uuid4))

    # Foreign key that references the 'id' column of the 'user' table
    id_user = Column(String, nullable=False)

    # Creation date, defaulting to the current timestamp
    creation_date = Column(DateTime, nullable=False)

    # File name
    name = Column(String, nullable=False)

    # File name
    url = Column(String, nullable=False, unique=True)

    # Define the foreign key constraint explicitly
    __table_args__ = (
        sa.ForeignKeyConstraint(["id_user"], ["user.id"], ondelete="CASCADE"),
    )
