from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import create_access_token, get_id_from_access_token, hash_password, verify_password
from app.models import User
from app.schemas.user import UserCreate, UserOut
from app.services.database_service import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


async def _get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def _get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def create_user(db: AsyncSession, new_user: UserCreate):
    existed_user = await _get_user_by_username(db, new_user.username);

    if (existed_user is not None):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Such user already exists")
    
    hashed_password = hash_password(new_user.password)
    user = User(username=new_user.username, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User | None :
    try:
        user_id = get_id_from_access_token(token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    try:
        user = await _get_user_by_id(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User is not found')
    
    return user


async def _get_user(db: AsyncSession, username: str, password: str) -> UserOut | None:
    user = await _get_user_by_username(db, username)
    if user and verify_password(password, str(user.hashed_password)):
        return UserOut(id=user.id, username=user.username)
    return None


async def login(db: AsyncSession, username: str, password: str):
    user = await _get_user(db, username, password)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")
    
    return create_access_token(dict(user))

