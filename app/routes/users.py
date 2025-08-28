from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import UserModel
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.auth_service import AuthService, CurrentUserService
from app.services.database_service import get_db


router = APIRouter(prefix="/users", tags=["users"])

@router.post('/register')
async def register(user: UserCreate, auth_service: AuthService = Depends(AuthService)) -> bool:
    await auth_service.register(user)
    return True


@router.post('/login')
async def login(user: UserLogin, auth_service: AuthService = Depends(AuthService)):
    access_token = await auth_service.login(username=user.username, password=user.password)
    return { "accessToken": access_token }


@router.get('/me', response_model=UserOut)
async def me(current_user_service: CurrentUserService = Depends(CurrentUserService)):
    return await current_user_service.get_current_user()
