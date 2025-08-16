from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.financial_operation import FinancialOperation
from app.models.user import User


def add_financial_operation(db: Session, user: User, amount: float):
    operation = FinancialOperation(amount = amount, user_id=user.id)
    db.add(operation)
    db.commit()
    db.refresh(operation)
    return operation


def get_all(db: Session, user: User, skip: int = 0, limit: int = 10):
    q = (
        select(FinancialOperation)
        .where(FinancialOperation.user_id == user.id)
        .order_by(FinancialOperation.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return db.execute(q).scalars().all()