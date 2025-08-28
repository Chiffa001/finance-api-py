from fastapi import Depends

from app.repositories.financial_operation_repository import FinancialOperationRepository
from app.services.auth_service import CurrentUserService


class FinancialOperationService:
    def __init__(self, repository: FinancialOperationRepository = Depends(), current_user_service: CurrentUserService = Depends(CurrentUserService)) -> None:
        self.repository = repository
        self.current_user_service = current_user_service


    async def add(self, amount: float):
        current_user = await self.current_user_service.get_current_user()
        operation = await self.repository.add(user_id=current_user.id, amount=amount)
        return operation
    

    async def get_all(self, skip: int = 0, limit: int = 10):
        current_user = await self.current_user_service.get_current_user()
        result = await self.repository.get_all(user_id=current_user.id, skip=skip, limit=limit)
        return result
        