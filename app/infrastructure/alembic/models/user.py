from sqlalchemy import Column, Integer, String
from app.infrastructure.alembic.models.base import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
