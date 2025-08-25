from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.operation import OperationBase
from app.services.auth_service import get_current_user
from app.services.database_service import get_db
from app.services.financial_operation_service import add_financial_operation, get_all as get_all_operations

router = APIRouter(prefix="/operations", tags=["operations"])

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_operation(operation: OperationBase, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> bool:
    await add_financial_operation(db, current_user, operation.amount)
    return True


@router.get("/all")
async def get_all(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_all_operations(skip=skip, limit=limit, db=db, user=current_user)