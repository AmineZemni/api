from enum import Enum
import pandas as pd
from fastapi import UploadFile, HTTPException
import logging
import os
import yaml
from typing import Dict, Any, List
import io


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# TODO : generate FileStructure enum from a list of yml validator file names
class FileStructure(Enum):
    aoc_step = "aoc_step"
    calc_process = "calc_process"
    cf_items = "cf_items"
    discount_types = "discount_types"
    reporting_process = "reporting_process"
    run_types = "run_types"
    timeframe = "timeframe"
    uao = "uao"
    lrc_input_proj = "lrc_input_proj"
    monthly_yield_curves = "monthly_yield_curves"


class CSVValidator:
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
        self.schemas = self._load_schemas()
        self.common_config = self._load_common_config()

    def _load_schemas(self) -> Dict[FileStructure, Dict[str, Any]]:
        yaml_path = os.path.join(os.path.dirname(__file__), "files_structures.yml")

        try:
            with open(yaml_path, "r") as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            raise RuntimeError(f"Schema file not found: {yaml_path}")

        schemas = {}
        for fs in config["file_structures"]:
            try:
                # Map YAML name to FileStructure enum
                fs_enum = FileStructure(fs["name"])
            except ValueError:
                continue  # Skip unknown structures

            # Process columns schema
            columns = {}
            for col_name, col_def in fs["schema"]["columns"].items():
                columns[col_name] = {
                    "types": [t.lower() for t in col_def["types"]],  # Normalize types
                    "nullable": col_def.get("nullable", False),
                }

            # Process CSV config with defaults
            csv_config = {"delimiter": ",", "encoding": "utf-8", "quotechar": '"'}
            csv_config.update(fs["schema"].get("csv_config", {}))

            schemas[fs_enum] = {
                "columns": columns,
                "csv_config": csv_config,
                "file_pattern": fs["file_pattern"],
            }

        return schemas

    def _load_common_config(self) -> Dict[str, Any]:
        yaml_path = os.path.join(os.path.dirname(__file__), "csv_schemas.yml")
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)

        return config.get("common_types", {})

    def validate(self, _file: UploadFile, file_structure: FileStructure) -> None:
        """Main validation entry point handling CSV structure and content"""
        if file_structure not in self.schemas:
            raise HTTPException(400, f"Unsupported file structure: {file_structure}")

        schema = self.schemas[file_structure]
        csv_config = schema.get("csv_config", {})
        errors = []

        try:
            # Read file content once and reset file pointer
            content = _file.file.read()
            _file.file.seek(0)  # Reset file pointer

            # Create a reusable file-like object
            file_stream = io.BytesIO(content)

            # Configure CSV reader with error handling and chunking
            reader = pd.read_csv(
                file_stream,
                chunksize=self.chunk_size,
                dtype=str,
                keep_default_na=False,
                na_filter=False,
                **csv_config,
            )

            for chunk_num, df in enumerate(reader):
                chunk_errors = []

                # Structural validation: Check column names and order
                chunk_errors += self._validate_columns(df, schema)

                # Content validation if structure is correct
                if not chunk_errors:
                    chunk_errors += self._validate_chunk_content(df, schema, chunk_num)

                errors += chunk_errors

            if errors:
                raise HTTPException(400, {"errors": errors})

        except pd.errors.EmptyDataError:
            raise HTTPException(400, "CSV file is empty")
        except pd.errors.ParserError as e:
            raise HTTPException(400, f"CSV parsing error: {str(e)}")
        except UnicodeDecodeError:
            raise HTTPException(
                400, f"Encoding error. Try {csv_config.get('encoding', 'utf-8')}"
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Validation error: {str(e)}", exc_info=True)
            raise HTTPException(500, "Internal validation error")

    def _validate_columns(self, df: pd.DataFrame, schema: Dict[str, Any]) -> List[str]:
        """Validate column names and order"""
        expected = list(schema["columns"].keys())
        actual = df.columns.tolist()
        errors = []
        if actual != expected:
            errors.append(f"Column mismatch. Expected: {expected}, Found: {actual}")
        return errors

    def _validate_chunk_content(
        self, df: pd.DataFrame, schema: Dict[str, Any], chunk_num: int
    ) -> List[str]:
        """Validate data types and constraints for a chunk"""
        errors = []
        # Header offset: Assuming header is on the first line of the file
        start_line = chunk_num * self.chunk_size + 2
        for idx, row in df.iterrows():
            line_number = start_line + idx
            for col, rules in schema["columns"].items():
                value = str(row.get(col, "")).strip()
                error = self._validate_value(value, col, rules, line_number)
                if error:
                    errors.append(error)
        return errors

    def _validate_value(
        self, value: str, column: str, rules: Dict[str, Any], line_number: int
    ) -> str:
        """Validate individual cell value"""
        # Null check
        if not value:
            if not rules.get("nullable", False):
                return f"L{line_number}: {column} cannot be empty"
            return ""
        # Type validation
        valid_type = False
        for dtype in rules["types"]:
            if self._check_type(value, dtype):
                valid_type = True
                break
        if not valid_type:
            return f"L{line_number}: {column} invalid value '{value}'. Expected types: {rules['types']}"
        return ""

    def _check_type(self, value: str, dtype: str) -> bool:
        """Type checking with format tolerance"""
        try:
            if dtype == "date":
                # Attempt flexible date parsing using common date formats
                for fmt in self.common_config.get("date_formats", ["%Y-%m-%d"]):
                    try:
                        pd.to_datetime(value, format=fmt)
                        return True
                    except ValueError:
                        continue
                return False
            elif dtype in ["int", "int64"]:
                return value.isdigit() or (
                    value.startswith("-") and value[1:].isdigit()
                )
            elif dtype in ["float", "int64"]:
                # Allow scientific notation and different decimal separators
                cleaned_value = value.replace(",", ".")
                float(cleaned_value)
                return True
            elif dtype == "str":
                return True
            return False
        except ValueError:
            return False


# Main validator instance for use in the controller
csvValidator = CSVValidator()
