from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database_service import get_db
from app.models.financial_operation_model import FinancialOperationModel


class FinancialOperationRepository:
    def __init__(self, db = Depends(get_db)) -> None:
        self.db: AsyncSession = db

    
    async def get_all(self, user_id: int, skip: int = 0, limit: int = 10):
        q = (
            select(FinancialOperationModel)
            .where(FinancialOperationModel.user_id == user_id)
            .order_by(FinancialOperationModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(q)
        return result.scalars().all()


    async def add(self, user_id: int, amount: float):
        operation = FinancialOperationModel(amount = amount, user_id=user_id)
        self.db.add(operation)
        await self.db.commit()
        await self.db.refresh(operation)
        return operation