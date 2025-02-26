# app/controllers/models.py
import uuid
from sqlalchemy import Column, Float
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.models.base import Base

from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()  # Define Base before using it in models


class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    x1 = Column(Float, nullable=False)
    x2 = Column(Float, nullable=False)
    sum = Column(Float, nullable=False)
