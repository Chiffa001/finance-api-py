from typing import Optional
from fastapi import Depends, HTTPException, status
from app.core.auth import hash_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)) -> None:
        self.user_repository = user_repository

    
    async def get_user(self, user_id: Optional[int] = None, username: Optional[str] = None):
        return await self.user_repository.get_user(user_id=user_id, username=username)


    async def create(self, new_user: UserCreate):
        is_user_exist = (await self.get_user(None, new_user.username)) is not None

        if (is_user_exist):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Such user already exists")
        

        hashed_password = hash_password(new_user.password)
        
        return await self.user_repository.create(username=new_user.username, hashed_password=hashed_password)
