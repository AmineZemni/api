import uuid
from app.domain.repositories.calculation_repository import CalculationRepository

class GetCalculationQuery:
    def __init__(self, repo: CalculationRepository):
        self.repo = repo

    async def execute(self, uid: uuid.UUID):
        return await self.repo.get_by_id(uid)
