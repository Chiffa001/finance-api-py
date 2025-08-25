from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.auth_service import get_current_user, login as user_login, create_user
from app.services.database_service import get_db


router = APIRouter(prefix="/users", tags=["users"])

@router.post('/register')
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)) -> bool:
    await create_user(db, user)
    return True


@router.post('/login')
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    access_token = await user_login(db, username=user.username, password=user.password)
    return { "accessToken": access_token }


@router.get('/me', response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
