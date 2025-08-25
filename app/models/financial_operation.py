from sqlalchemy import Integer, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class FinancialOperation(Base):
    __tablename__ = 'financial_operations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="operations") # type: ignore