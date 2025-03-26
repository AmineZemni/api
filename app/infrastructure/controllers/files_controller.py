from typing import List
from fastapi import APIRouter, Query

from app.application.query.get_files_by_user_query_handler import (
    FilesQueryModel,
    GetFilesQuery,
    getFilesQueryHandler,
)


files_router = APIRouter()


@files_router.get("/files", response_model=List[FilesQueryModel])
async def get_files(
    user_id: str = Query(..., description="The user id to retrieve files for")
):
    query = GetFilesQuery(user_id=user_id)
    return getFilesQueryHandler.execute(query)
