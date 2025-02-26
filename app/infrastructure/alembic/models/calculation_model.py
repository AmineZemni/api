import uuid
from sqlalchemy import Column, Float
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.models.base import Base


class CalculationModel(Base):
    __tablename__ = "calculations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    x1 = Column(Float, nullable=False)
    x2 = Column(Float, nullable=False)
    result = Column(Float, nullable=False)
