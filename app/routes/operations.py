from fastapi import APIRouter, Depends, Query, status

from app.schemas.operation import OperationBase
from app.services.financial_operation_service import FinancialOperationService

router = APIRouter(prefix="/operations", tags=["operations"])

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_operation(operation: OperationBase, financial_operation_service: FinancialOperationService = Depends(FinancialOperationService)) -> bool:
    await financial_operation_service.add(amount=operation.amount)
    return True


@router.get("/all")
async def get_all(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), financial_operation_service: FinancialOperationService = Depends(FinancialOperationService)):
    return await financial_operation_service.get_all(skip=skip, limit=limit)