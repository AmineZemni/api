from typing import List
from fastapi import APIRouter, Query, UploadFile, Form, File

from app.application.commands.upload_file_query_handler import (
    UploadFileCommand,
    uploadFileCommandHandler,
)
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


@files_router.post("/files", response_model=None)
async def post_file(
    file: UploadFile = File(...),
    file_structure: str = Form(...),
    user_id: str = Form(...),
):
    command = UploadFileCommand(
        file=file, file_structure=file_structure, user_id=user_id
    )

    uploadFileCommandHandler.execute(command)
