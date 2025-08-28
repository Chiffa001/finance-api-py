from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.auth import create_access_token, get_id_from_access_token, verify_password
from app.models import UserModel
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


class CurrentUserService:
    def __init__(self, user_service: UserService = Depends(UserService), token: str = Depends(oauth2_scheme)) -> None:
        self.user_service = user_service;
        self.token = token

    
    async def get_current_user(self) -> UserModel:
        try:
            user_id = get_id_from_access_token(self.token)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
        try:
            user = await self.user_service.get_user(user_id=user_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User is not found')
        
        return user

class AuthService:
    def __init__(self, user_service: UserService = Depends(UserService)) -> None:
        self.user_service = user_service


    async def register(self, new_user: UserCreate):
        return await self.user_service.create(new_user)
    

    async def login(self, username: str, password: str):
        user = await self.user_service.get_user(username=username)

        if user and verify_password(password, str(user.hashed_password)):
            return create_access_token(dict(UserOut(username=user.username, id=user.id)))

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")
