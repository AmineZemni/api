from fastapi import HTTPException
from pydantic import BaseModel
from app.application.types import QueryHandler
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from uuid import UUID

from app.database import DatabaseService
from app.infrastructure.alembic.models.user import User


class GetUserByKeyQuery(BaseModel):
    key: str


class UserQueryModel(BaseModel):
    id: UUID
    name: str


db_service = DatabaseService()


class GetUserByKeyQueryHandler(QueryHandler):
    def execute(self, query: GetUserByKeyQuery) -> UserQueryModel:
        session: Session = db_service.get_session()

        try:
            # Query the database to find the user by the provided key
            user = (
                session.query(User).filter(User.key == query.key).one()
            )  # Change 'key' to the actual column name

            # Map the user to UserQueryModel
            user_model = UserQueryModel(id=user.id, name=user.name)

            return user_model

        except NoResultFound:
            # If no user found, handle appropriately (e.g., raise an exception or return None)
            raise HTTPException(
                status_code=404,
                detail=f"User not found with key {query.key}",
            )
        finally:
            session.close()


getUserByKeyQueryHandler = GetUserByKeyQueryHandler()
