from app.application.types import Command


class AddValuesCommandHandler(Command):
    def execute(self, value1: float, value2: float) -> float:
        return value1 + value2


addValuesCommandHandler = AddValuesCommandHandler()
