import uuid
from sqlalchemy import Column, Integer
from database import db
from sqlalchemy.dialects.postgresql import UUID


class CalculationModel(db.Model):
    __tablename__ = "calculations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    value1 = Column(Integer, nullable=False)
    value2 = Column(Integer, nullable=False)
    result = Column(Integer, nullable=False)
