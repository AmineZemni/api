from app.application.commands.add_values_command_handler import addValuesCommandHandler
from app.infrastructure.controllers.request_schemas import CalculationSampleRequest


def should_return_addition_result():
    # Given
    command = CalculationSampleRequest(
        value1=50,
        value2=20,
    )

    # When
    result = addValuesCommandHandler.execute(command)

    # Then
    assert result == 70
