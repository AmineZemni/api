from sqlalchemy import Column, String
from app.infrastructure.alembic.models.base import Base
import uuid


class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    key = Column(String, nullable=False, unique=True)
