from app.domain.entities.calculation import Calculation
from app.domain.repositories.calculation_repository import CalculationRepository
import uuid

from app.infrastructure.models.session import async_session


class CreateCalculationCommand:
    def __init__(self, repo: CalculationRepository):
        self.repo = repo

    async def execute(self, x1: float, x2: float) -> Calculation:
        calculation = Calculation(id=uuid.uuid4(), x1=x1, x2=x2, result=x1 + x2)
        return await self.repo.save(calculation)
