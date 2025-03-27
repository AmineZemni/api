from fastapi import UploadFile
from pydantic import BaseModel
from app.application.types import CommandHandler
from sqlalchemy.orm import Session
from app.database import DatabaseService
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import insert

from app.infrastructure.alembic.models.file import FileMetadata
from app.infrastructure.services.firebase_service import (
    firebase_client,
)
from app.application.commands.validators.csv_validator import csvValidator


class UploadFileCommand(BaseModel):
    file: UploadFile
    file_structure: str
    user_id: str


db_service = DatabaseService()


class UploadFileCommandHandler(CommandHandler):
    def execute(self, command: UploadFileCommand) -> None:
        csvValidator.validate(command.file, command.file_structure)

        # Get the session from the database service
        session: Session = db_service.get_session()

        # Generate a file path for Firebase based on user_id and file_structure
        file_name = f"{command.user_id}/inputs/{command.file_structure}.csv"

        # Upload the file to Firebase and get the public URL
        file_url = firebase_client.upload_file_and_get_public_url(
            command.file, file_name
        )

        # Create a unique ID for the file metadata
        file_id = str(uuid.uuid4())

        # Prepare the file metadata
        file_metadata = {
            "id": file_id,
            "id_user": command.user_id,
            "creation_date": datetime.now(),
            "name": command.file_structure,
            "url": file_url,
        }

        # Save the file metadata in the database (Assuming there's a function for saving this data)
        self.save_file_metadata(session, file_metadata)

    def save_file_metadata(self, session: Session, file_metadata: dict) -> None:
        # Build the INSERT statement with conflict handling
        stmt = insert(FileMetadata).values(file_metadata)

        # Handle the conflict on 'name' and update other fields
        stmt = stmt.on_conflict_do_update(
            index_elements=["url"],  # Define conflict on 'name' column
            set_={
                "id_user": file_metadata["id_user"],
                "creation_date": file_metadata["creation_date"],
                "name": file_metadata["name"],
            },
        )

        # Execute the statement
        session.execute(stmt)
        session.commit()


# Instantiate the command handler
uploadFileCommandHandler = UploadFileCommandHandler()
