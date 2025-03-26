from sqlalchemy import Column, String
from app.infrastructure.alembic.models.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    key = Column(String, nullable=False)
