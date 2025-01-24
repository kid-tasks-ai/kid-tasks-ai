from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.reward import RewardCreate, RewardUpdate, RewardResponse
from app.schemas.user import UserResponse
from app.crud import reward as reward_crud

router = APIRouter()


@router.post("", response_model=RewardResponse)
async def create_reward(
        reward: RewardCreate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Создание новой награды"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только родители могут создавать награды"
        )
    return reward_crud.create_reward(db, reward)


@router.get("", response_model=List[RewardResponse])
async def get_rewards(
        child_id: int,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        is_redeemed: Optional[bool] = None,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение списка наград"""
    if current_user.role == "child" and current_user.id != child_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете видеть только свои награды"
        )
    return reward_crud.get_rewards(
        db,
        child_id=child_id,
        skip=skip,
        limit=limit,
        is_active=is_active,
        is_redeemed=is_redeemed
    )


@router.get("/{reward_id}", response_model=RewardResponse)
async def get_reward(
        reward_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение награды по ID"""
    reward = reward_crud.get_reward(db, reward_id)
    if not reward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Награда не найдена"
        )

    # Проверяем доступ для ребенка
    if current_user.role == "child" and current_user.id != reward.child_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете видеть только свои награды"
        )
    return reward


@router.put("/{reward_id}", response_model=RewardResponse)
async def update_reward(
        reward_id: int,
        reward_data: RewardUpdate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Обновление награды"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только родители могут обновлять награды"
        )

    updated_reward = reward_crud.update_reward(db, reward_id, reward_data)
    if not updated_reward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Награда не найдена"
        )
    return updated_reward


@router.delete("/{reward_id}")
async def delete_reward(
        reward_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Удаление награды"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только родители могут удалять награды"
        )

    if not reward_crud.delete_reward(db, reward_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Награда не найдена"
        )
    return {"status": "success"}


@router.post("/{reward_id}/redeem", response_model=RewardResponse)
async def redeem_reward(
        reward_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Погашение награды"""
    if current_user.role != "child":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только дети могут погашать награды"
        )

    redeemed_reward = reward_crud.redeem_reward(db, reward_id, current_user.id)
    if not redeemed_reward:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось погасить награду. Проверьте баланс баллов и статус награды."
        )
    return redeemed_reward