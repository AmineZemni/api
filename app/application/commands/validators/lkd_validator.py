import pandas as pd
import yaml
import os
import io
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LKDValidationService:
    def __init__(self, yaml_file="csv_schemas.yml"):
        self.csv_schemas = self._load_csv_schemas(yaml_file)

    def _load_csv_schemas(self, yaml_file: str) -> dict:
        """Load CSV schemas from a YAML file."""
        yaml_path = os.path.join(os.path.dirname(__file__), yaml_file)

        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"YAML file '{yaml_path}' not found.")

        with open(yaml_path, "r") as file:
            config = yaml.safe_load(file)

        return config["csv_files"]

    async def _validate_csv(
        self, file: UploadFile, csv_type: str
    ) -> Tuple[bool, str, Optional[int]]:
        """Validates CSV structure and data types with detailed error tracking."""
        logger.info(f"Validating CSV file: {csv_type}")
        if csv_type not in self.csv_schemas:
            return False, f"CSV type '{csv_type}' not defined in YAML", None

        expected_columns = self.csv_schemas[csv_type]["columns"]
        logger.info(f"Expected columns: {expected_columns}")

        try:
            # Read the file in chunks to track line numbers
            content = await file.read()
            await file.seek(0)

            # Use StringIO to simulate a file-like object
            file_like = io.StringIO(content.decode("utf-8"))

            # Read the file in chunks
            chunk_size = 1000  # Adjust based on file size
            reader = pd.read_csv(file_like, chunksize=chunk_size)

            for chunk_number, df in enumerate(reader):
                # Track the starting line number for the chunk
                start_line = chunk_number * chunk_size + 1

                # Validate columns
                if set(df.columns) != set(expected_columns.keys()):
                    return (
                        False,
                        f"Invalid columns in {csv_type}: Expected {set(expected_columns.keys())}, Found {set(df.columns)}",
                        start_line,
                    )

                # Validate data types for each column
                for column, column_rules in expected_columns.items():
                    logger.info(
                        f"Validating column '{column}' with rules: {column_rules}"
                    )
                    acceptable_types = column_rules.get("types", [])
                    if not acceptable_types:
                        return (
                            False,
                            f"No data types defined for column '{column}' in YAML",
                            start_line,
                        )

                    # Check each value in the column
                    for index, value in df[column].items():
                        line_number = start_line + index
                        is_valid = False

                        # Check for NaN values and treat them as an empty string or a valid placeholder value
                        if pd.isna(value):
                            value = ""  # Or handle NaN as needed

                        for expected_dtype in acceptable_types:
                            if expected_dtype == "date":
                                try:
                                    pd.to_datetime(value, dayfirst=True, errors="raise")
                                    is_valid = True
                                    break
                                except ValueError:
                                    continue
                            elif expected_dtype == "int64":
                                try:
                                    if not isinstance(value, int) and not (
                                        isinstance(value, str) and value.isdigit()
                                    ):
                                        raise ValueError
                                    is_valid = True
                                    break
                                except ValueError:
                                    continue
                            elif expected_dtype == "float":
                                try:
                                    if not isinstance(value, float) and not (
                                        isinstance(value, str)
                                        and value.replace(".", "", 1).isdigit()
                                    ):
                                        raise ValueError
                                    is_valid = True
                                    break
                                except ValueError:
                                    continue
                            elif expected_dtype == "str":
                                if isinstance(value, str):
                                    is_valid = True
                                    break

                        if not is_valid:
                            return (
                                False,
                                f"Invalid data type in {csv_type}, column '{column}', line {line_number}: Expected {acceptable_types}, Found {type(value).__name__}",
                                line_number,
                            )

            return True, "CSV is valid", None

        except pd.errors.EmptyDataError:
            return False, f"CSV file '{csv_type}' is empty", None
        except Exception as e:
            return False, f"Error validating {csv_type}: {str(e)}", None

    async def validate_lkd_input_files(
        self,
        aoc_step,
        calc_process,
        cf_items,
        discount_types,
        reporting_process,
        run_types,
        timeframe,
        uao,
        lrc_input_proj,
        monthly_yield_curves,
    ):
        """Validate all input files for LKD calculation."""
        files = {
            "aoc_step.csv": aoc_step,
            "calc_process.csv": calc_process,
            "cf_items.csv": cf_items,
            "discount_types.csv": discount_types,
            "reporting_process.csv": reporting_process,
            "run_types.csv": run_types,
            "timeframe.csv": timeframe,
            "uao.csv": uao,
            "lrc_input_proj.csv": lrc_input_proj,
            "monthly_yield_curves.csv": monthly_yield_curves,
        }

        for csv_type, file in files.items():
            is_valid, error, line_number = await self._validate_csv(file, csv_type)
            if not is_valid:
                # Raise HTTPException with 400 status and detailed error message
                raise HTTPException(
                    status_code=400,
                    detail=f"Validation failed for {csv_type}: {error}",
                )

            # Reset file pointer for further processing
            await file.seek(0)


lKDValidationService = LKDValidationService()
