from app.application.types import CommandHandler
from app.infrastructure.controllers.request_schemas import CalculationSampleRequest


class AddValuesCommandHandler(CommandHandler):
    def execute(self, command: CalculationSampleRequest) -> float:
        return command.value1 + command.value2


addValuesCommandHandler = AddValuesCommandHandler()
