from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.financial_operation import FinancialOperation
from app.models.user import User


async def add_financial_operation(db: AsyncSession, user: User, amount: float):
    operation = FinancialOperation(amount = amount, user_id=user.id)
    db.add(operation)
    await db.commit()
    await db.refresh(operation)
    return operation


async def get_all(db: AsyncSession, user: User, skip: int = 0, limit: int = 10):
    q = (
        select(FinancialOperation)
        .where(FinancialOperation.user_id == user.id)
        .order_by(FinancialOperation.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(q);
    return result.scalars().all()