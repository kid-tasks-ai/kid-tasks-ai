from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.child import ChildCreate, ChildUpdate, ChildResponse
from app.crud import child as child_crud
from app.schemas.user import UserResponse

router = APIRouter()


@router.post("", response_model=ChildResponse)
async def create_child_profile(
        child_data: ChildCreate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Создание профиля ребенка"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=403,
            detail="Только родители могут создавать профили детей"
        )

    # Проверяем, не занят ли email
    existing_user = child_crud.get_user_by_email(db, email=child_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email уже зарегистрирован"
        )

    return child_crud.create_child(db, child_data, current_user.id)


@router.get("", response_model=List[ChildResponse])
async def get_children_profiles(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение списка профилей детей текущего родителя"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=403,
            detail="Доступно только для родителей"
        )

    return child_crud.get_children(db, current_user.id)


@router.get("/{child_id}", response_model=ChildResponse)
async def get_child_profile(
        child_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение информации о конкретном профиле ребенка"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=403,
            detail="Доступно только для родителей"
        )

    child = child_crud.get_child(db, child_id, current_user.id)
    if not child:
        raise HTTPException(
            status_code=404,
            detail="Профиль ребенка не найден"
        )

    return child


@router.put("/{child_id}", response_model=ChildResponse)
async def update_child_profile(
        child_id: int,
        child_data: ChildUpdate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Обновление профиля ребенка"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=403,
            detail="Доступно только для родителей"
        )

    updated_child = child_crud.update_child(db, child_id, current_user.id, child_data)
    if not updated_child:
        raise HTTPException(
            status_code=404,
            detail="Профиль ребенка не найден"
        )

    return updated_child


@router.delete("/{child_id}")
async def delete_child_profile(
        child_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Удаление профиля ребенка"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=403,
            detail="Доступно только для родителей"
        )

    success = child_crud.delete_child(db, child_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Профиль ребенка не найден"
        )

    return {"status": "success", "message": "Профиль ребенка удален"}