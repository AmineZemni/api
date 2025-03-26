from typing import List
from fastapi import HTTPException
from pydantic import BaseModel
from app.application.types import QueryHandler
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from uuid import UUID

from app.database import DatabaseService
from app.infrastructure.alembic.models.file import File


class GetFilesQuery(BaseModel):
    user_id: str


class FilesQueryModel(BaseModel):
    url: str
    name: str


db_service = DatabaseService()


class GetFilesQueryHandler(QueryHandler):
    def execute(self, query: GetFilesQuery) -> List[FilesQueryModel]:
        session: Session = db_service.get_session()

        try:
            files_metadata = (
                session.query(File).filter(File.id_user == query.user_id).all()
            )

            return (
                [{"name": file["name"], "url": "unknown"} for file in files_metadata]
                if files_metadata
                else []
            )

        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail=f"No files not found with key {query.user_id}",
            )
        finally:
            session.close()


getFilesQueryHandler = GetFilesQueryHandler()
