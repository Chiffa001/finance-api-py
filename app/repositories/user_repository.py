from typing import Optional
from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import UserModel
from app.services.database_service import get_db


class UserRepository:
    def __init__(self, db = Depends(get_db)) -> None:
        self.db: AsyncSession = db

    
    async def create(self, username: str, hashed_password: str) -> UserModel:
        user = UserModel(username=username, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_user(self, user_id: Optional[int] = None, username: Optional[str] = None):
        if user_id is None and username is None:
            return None

        stmt = select(UserModel).where(
            or_(
                UserModel.id == user_id if user_id is not None else False,
                UserModel.username == username
            )
        )

        result = await self.db.execute(stmt)
        return result.scalars().first()