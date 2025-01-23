# app/api/v1/auth.py
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import get_settings
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import TokenResponse, RefreshToken
from app.crud import user as user_crud
from app.core import security

settings = get_settings()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


@router.post("/login", response_model=TokenResponse)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    user = user_crud.authenticate(
        db=db,
        email=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)  # Уменьшаем время жизни access токена
    refresh_token_expires = timedelta(days=30)  # Долгоживущий refresh токен

    access_token = security.create_access_token(
        user_id=user.id,
        role=user.role,
        expires_delta=access_token_expires
    )

    refresh_token = security.create_refresh_token(
        user_id=user.id,
        expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        refresh_token: str,
        db: Session = Depends(get_db)
):
    try:
        # Проверяем refresh токен
        payload = security.verify_refresh_token(refresh_token)
        user = user_crud.get_user(db, user_id=payload.get("user_id"))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден"
            )

        # Создаем новые токены
        access_token_expires = timedelta(minutes=30)
        refresh_token_expires = timedelta(days=30)

        access_token = security.create_access_token(
            user_id=user.id,
            role=user.role,
            expires_delta=access_token_expires
        )

        new_refresh_token = security.create_refresh_token(
            user_id=user.id,
            expires_delta=refresh_token_expires
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "role": user.role
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный refresh токен"
        )


@router.get("/verify")
async def verify_token(
        current_user: Annotated[UserResponse, Depends(security.get_current_user)]
):
    """Эндпоинт для проверки валидности токена"""
    return {"status": "valid"}