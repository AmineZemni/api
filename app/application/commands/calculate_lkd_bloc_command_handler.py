from app.application.types import Command


class CalculateLKDBlocCommandHandler(Command):
    def execute(self) -> str:
        calculationId = "test"

        # TODO : read CSV and call calculate_lkd_bloc from package

        return calculationId


calculateLKDBlocCommandHandler = CalculateLKDBlocCommandHandler()
