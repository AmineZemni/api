import pandas as pd
from app.application.types import Command
from ifrs_17_engine.blocs.main_blocs import calculate_lkd_bloc
from ifrs_17_engine.blocs.calculation_indicators import calc_calculation_indicators
from ifrs_17_engine.blocs.coverage_indicators import calc_indicators
from ifrs_17_engine.blocs.timeframe import calc_timeframe
from ifrs_17_engine.tools.cashflow_transformation import transform_cashflow_projection


class CalculateLKDBlocCommandHandler(Command):
    def execute(self) -> str:
        calculationId = "test"

        # TODO : read CSV from API input not from filesystem

        aoc_step_path = "app/test_data/inputs/aoc_step.csv"
        calc_process_path = "app/test_data/inputs/calc_process.csv"
        cf_items_path = "app/test_data/inputs/cf_items.csv"
        discount_types_path = "app/test_data/inputs/discount_types.csv"
        reporting_process_path = "app/test_data/inputs/reporting_process.csv"
        run_types_path = "app/test_data/inputs/run_types.csv"
        timeframe_path = "app/test_data/inputs/timeframe.csv"
        uao_path = "app/test_data/inputs/uao.csv"
        lrc_input_proj_path = "app/test_data/inputs/lrc_input_proj.csv"
        monthly_yield_curves_path = "app/test_data/inputs/monthly_yield_curves.csv"

        aoc_step_df = pd.read_csv(aoc_step_path)
        calc_process_df = pd.read_csv(
            calc_process_path,
            parse_dates=["calc_start_date", "calc_end_date"],
            dayfirst=True,
        )

        cf_items_df = pd.read_csv(cf_items_path)
        discount_types_df = pd.read_csv(discount_types_path)
        reporting_process_df = pd.read_csv(
            reporting_process_path,
            parse_dates=["reporting_opening_date", "reporting_closing_date"],
            dayfirst=True,
        )
        run_types_df = pd.read_csv(run_types_path)
        timeframe_df = pd.read_csv(
            timeframe_path, parse_dates=["timeframe_start_date"], dayfirst=True
        )
        uao_df = pd.read_csv(
            uao_path,
            parse_dates=["uoa_initrecog_date", "uoa_expiry_date"],
            dayfirst=True,
        )
        lrc_input_proj_df = pd.read_csv(lrc_input_proj_path)
        monthly_yield_curves_df = pd.read_csv(monthly_yield_curves_path)

        # convert to dict
        timeframe_dict = timeframe_df.to_dict(orient="records")
        calc_process_dict = calc_process_df.to_dict(orient="records")
        reporting_process_dict = reporting_process_df.to_dict(orient="records")
        uao_dict = uao_df.to_dict(orient="records")

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

        ic_lrc_prm_lkd_m_aoc_df.to_csv(
            "app/test_data/outputs/ic_lrc_prm_lkd_m_aoc.csv",
            sep=";",
            decimal=",",
            index=False,
        )

        return calculationId


calculateLKDBlocCommandHandler = CalculateLKDBlocCommandHandler()
