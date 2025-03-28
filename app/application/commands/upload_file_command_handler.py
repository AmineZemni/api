from fastapi import UploadFile, HTTPException
from pydantic import BaseModel
from app.application.types import CommandHandler
from sqlalchemy.orm import Session
from app.database import DatabaseService
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert

from app.infrastructure.alembic.models.file import FileMetadata
from app.infrastructure.alembic.models.user import User
from app.infrastructure.services.firebase_service import (
    firebase_client,
)
from app.application.commands.validators.csv_validator import (
    csvValidator,
    FileStructure,
)


class UploadFileCommand(BaseModel):
    file: UploadFile
    file_structure: str
    user_id: str


db_service = DatabaseService()


class UploadFileCommandHandler(CommandHandler):
    def execute(self, command: UploadFileCommand) -> None:
        # Get the session from the database service
        session: Session = db_service.get_session()

        # check if user_id is valid
        user = session.query(User).filter(User.id == command.user_id).first()
        if not user:
            raise HTTPException(404, f"User with id {command.user_id} not found.")

        # Convert file_structure string to FileStructure enum
        try:
            file_structure_enum = FileStructure(command.file_structure)
        except ValueError:
            raise HTTPException(
                400, f"Unsupported file structure: {command.file_structure}"
            )

        # On passe ici l'enum plutôt que la chaîne brute
        csvValidator.validate(command.file, file_structure_enum)

        # Generate a file path for Firebase based on user_id and file_structure
        file_name = f"{command.user_id}/inputs/{command.file_structure}.csv"

        # Upload the file to Firebase and get the public URL
        file_url = firebase_client.upload_file_and_get_public_url(
            command.file, file_name
        )

        # Prepare the file metadata
        file_metadata = {
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
