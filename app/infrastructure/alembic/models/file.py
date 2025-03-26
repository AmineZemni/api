from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.alembic.models.base import Base
import uuid
import sqlalchemy as sa


class File(Base):
    __tablename__ = "file"

    # UUID primary key with default value generation
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign key that references the 'id' column of the 'user' table
    id_user = Column(UUID(as_uuid=True), nullable=False)

    # Creation date, defaulting to the current timestamp
    creation_date = Column(DateTime, nullable=False, default=uuid.uuid4)

    # File name
    name = Column(String, nullable=False)

    # Define the foreign key constraint explicitly
    __table_args__ = (
        sa.ForeignKeyConstraint(["id_user"], ["user.id"], ondelete="CASCADE"),
    )
