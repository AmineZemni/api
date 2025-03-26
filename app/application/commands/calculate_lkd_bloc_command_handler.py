import pandas as pd
from ifrs_17_engine.blocs.main_blocs import calculate_lkd_bloc
from ifrs_17_engine.blocs.calculation_indicators import calc_calculation_indicators
from ifrs_17_engine.blocs.coverage_indicators import calc_indicators
from ifrs_17_engine.blocs.timeframe import calc_timeframe
from ifrs_17_engine.tools.cashflow_transformation import transform_cashflow_projection
from app.application.types import CommandHandler
from app.infrastructure.controllers.request_schemas import CalculationLKDRequest
from app.application.commands.validators.lkd_validator import lKDValidationService


class CalculateLKDBlocCommandHandler(CommandHandler):
    async def execute(
        self,
        command: CalculationLKDRequest,
    ) -> str:
        """Execute the LKD calculation using uploaded CSV files."""

        await lKDValidationService.validate_lkd_input_files(
            command.aoc_step_file,
            command.calc_process_file,
            command.cf_items_file,
            command.discount_types_file,
            command.reporting_process_file,
            command.run_types_file,
            command.timeframe_file,
            command.uao_file,
            command.lrc_input_proj_file,
            command.monthly_yield_curves_file,
        )

        calculation_id = "test"

        # Read CSV files from UploadFile objects
        aoc_step_df = pd.read_csv(command.aoc_step_file.file)
        calc_process_df = pd.read_csv(
            command.calc_process_file.file,
            parse_dates=["calc_start_date", "calc_end_date"],
            dayfirst=True,
        )
        cf_items_df = pd.read_csv(command.cf_items_file.file)
        discount_types_df = pd.read_csv(command.discount_types_file.file)
        reporting_process_df = pd.read_csv(
            command.reporting_process_file.file,
            parse_dates=["reporting_opening_date", "reporting_closing_date"],
            dayfirst=True,
        )
        run_types_df = pd.read_csv(command.run_types_file.file)
        timeframe_df = pd.read_csv(
            command.timeframe_file.file,
            parse_dates=["timeframe_start_date"],
            dayfirst=True,
        )
        uao_df = pd.read_csv(
            command.uao_file.file,
            parse_dates=["uoa_initrecog_date", "uoa_expiry_date"],
            dayfirst=True,
        )
        lrc_input_proj_df = pd.read_csv(command.lrc_input_proj_file.file)
        monthly_yield_curves_df = pd.read_csv(command.monthly_yield_curves_file.file)

        # Convert to dict
        timeframe_dict = timeframe_df.to_dict(orient="records")
        calc_process_dict = calc_process_df.to_dict(orient="records")
        reporting_process_dict = reporting_process_df.to_dict(orient="records")
        uao_dict = uao_df.to_dict(orient="records")

        # Perform calculations
        timeframe_generated_df = calc_timeframe(timeframe_dict[0])
        calculation_indicators_df = calc_calculation_indicators(
            calc_process_dict[0], reporting_process_dict[0], timeframe_generated_df
        )
        coverage_indicators_df = calc_indicators(
            uao_dict[0], timeframe_generated_df, calculation_indicators_df
        )
        cf_proj_df = transform_cashflow_projection(
            lrc_input_proj_df, calculation_indicators_df
        )
        ic_lrc_prm_lkd_m_aoc_df = calculate_lkd_bloc(
            calculation_indicators_df,
            coverage_indicators_df,
            monthly_yield_curves_df,
            cf_proj_df,
        )

        # Save output to CSV
        ic_lrc_prm_lkd_m_aoc_df.to_csv(
            "app/test_data/outputs/ic_lrc_prm_lkd_m_aoc.csv",
            sep=";",
            decimal=",",
            index=False,
        )

        return calculation_id


calculateLKDBlocCommandHandler = CalculateLKDBlocCommandHandler()
