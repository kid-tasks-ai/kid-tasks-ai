# app/api/v1/child.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.task import TaskAssignmentResponse
from app.schemas.reward import RewardResponse
from app.schemas.user import UserResponse
from app.schemas.child import ChildResponse
from app.crud import task as task_crud
from app.crud import reward as reward_crud

router = APIRouter()


@router.get("/tasks", response_model=List[TaskAssignmentResponse])
async def get_my_tasks(
        is_completed: bool | None = None,
        is_approved: bool | None = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение заданий текущего пользователя (ребенка)"""
    print(current_user)
    if current_user.role != "child":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для детей"
        )

    return task_crud.get_task_assignments(
        db,
        child_id=current_user.id,
        is_completed=is_completed,
        is_approved=is_approved,
        skip=skip,
        limit=limit
    )


@router.get("/tasks/{task_id}", response_model=TaskAssignmentResponse)
async def get_my_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение конкретного задания текущего пользователя"""
    if current_user.role != "child":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для детей"
        )

    task = task_crud.get_task_assignment(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задание не найдено"
        )

    if task.child_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому заданию"
        )

    return task


@router.post("/tasks/{task_id}/complete", response_model=TaskAssignmentResponse)
async def complete_my_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Отметить задание как выполненное"""
    if current_user.role != "child":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для детей"
        )

    task = task_crud.get_task_assignment(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задание не найдено"
        )

    if task.child_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому заданию"
        )

    if task.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Задание уже отмечено как выполненное"
        )

    return task_crud.complete_task(db, task_id)


@router.get("/rewards", response_model=List[RewardResponse])
async def get_my_rewards(
        is_redeemed: bool | None = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение наград текущего пользователя"""
    if current_user.role != "child":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для детей"
        )

    return reward_crud.get_rewards(
        db,
        child_id=current_user.id,
        is_redeemed=is_redeemed,
        skip=skip,
        limit=limit
    )


@router.post("/rewards/{reward_id}/redeem", response_model=RewardResponse)
async def redeem_my_reward(
        reward_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получить награду"""
    if current_user.role != "child":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для детей"
        )

    reward = reward_crud.get_reward(db, reward_id)
    if not reward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Награда не найдена"
        )

    if reward.child_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этой награде"
        )

    redeemed_reward = reward_crud.redeem_reward(db, reward_id, current_user.id)
    if not redeemed_reward:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось получить награду. Проверьте баланс баллов."
        )

    return redeemed_reward


@router.get("", response_model=ChildResponse)
async def get_my_profile(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение профиля текущего пользователя (ребенка)"""
    if current_user.role != "child":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для детей"
        )

    return current_user