from enum import Enum
from fastapi import UploadFile, HTTPException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileStructure(Enum):
    aoc_step = "aoc_step"


class CSVValidator:
    def __init__(self):
        pass

    def validate(self, _file: UploadFile, file_structure: FileStructure) -> None:
        if file_structure == FileStructure.aoc_step:
            print("Validating AOC Step file")
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown file structure {file_structure}",
            )


csvValidator = CSVValidator()
