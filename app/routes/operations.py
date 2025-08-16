from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.operation import OperationBase
from app.services.auth_service import get_current_user
from app.services.database_service import get_db
from app.services.financial_operation_service import add_financial_operation, get_all as get_all_operations

router = APIRouter(prefix="/operations", tags=["operations"])

@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_operation(operation: OperationBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> bool:
    add_financial_operation(db, current_user, operation.amount)
    return True


@router.get("/all")
def get_all(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_operations(skip=skip, limit=limit, db=db, user=current_user)