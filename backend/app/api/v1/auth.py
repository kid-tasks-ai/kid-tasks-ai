from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import get_settings
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as user_crud
from app.core import security

settings = get_settings()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


@router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    """
    Вход в систему для получения токена доступа.
    Поддерживает как родителей, так и детей.
    """
    user = user_crud.authenticate(
        db=db,
        email=form_data.username,  # OAuth2 использует username, но мы используем email
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаем access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user_id=user.id, role=user.role, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя (только родителя).
    Дети создаются через отдельный эндпоинт после аутентификации родителя.
    """
    # Проверяем, не занят ли email
    existing_user = user_crud.get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )

    # Создаем нового пользователя
    user = user_crud.create_user(db, user_data)
    return user


@router.get("/me", response_model=UserResponse)
async def read_users_me(
        current_user: Annotated[UserResponse, Depends(security.get_current_user)]
):
    """
    Получение информации о текущем пользователе
    """
    return current_user