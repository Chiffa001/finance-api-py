from pydantic import BaseModel


class OperationBase(BaseModel):
    amount: float