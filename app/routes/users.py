from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.auth_service import get_current_user, login as user_login, create_user
from app.services.database_service import get_db


router = APIRouter(prefix="/users", tags=["users"])

@router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)) -> bool:
    create_user(db, user)
    return True


@router.post('/login')
def login(user: UserLogin, db: Session = Depends(get_db)):
    access_token = user_login(db, username=user.username, password=user.password)
    return { "accessToken": access_token }


@router.get('/me')
def me(current_user: User = Depends(get_current_user)):
    return UserOut(id=current_user.id, username=current_user.username)
