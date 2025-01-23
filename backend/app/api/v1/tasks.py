# app/api/v1/tasks.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.task import (
    TaskTemplateCreate,
    TaskTemplateUpdate,
    TaskTemplateResponse,
    TaskAssignmentCreate,
    TaskAssignmentUpdate,
    TaskAssignmentResponse
)
from app.schemas.user import UserResponse
from app.crud import task as task_crud

router = APIRouter()


# Шаблоны задач

@router.post("/templates", response_model=TaskTemplateResponse)
async def create_template(
        template: TaskTemplateCreate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Создание нового шаблона задачи"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только родители могут создавать шаблоны задач"
        )
    return task_crud.create_task_template(db, template)


@router.get("/templates", response_model=List[TaskTemplateResponse])
async def get_templates(
        child_id: int,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        category: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение списка шаблонов задач"""
    if current_user.role not in ["parent", "child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен"
        )
    return task_crud.get_task_templates(
        db,
        child_id=child_id,
        skip=skip,
        limit=limit,
        is_active=is_active,
        category=category
    )


@router.get("/templates/{template_id}", response_model=TaskTemplateResponse)
async def get_template(
        template_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение шаблона задачи по ID"""
    template = task_crud.get_task_template(db, template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Шаблон задачи не найден"
        )
    return template


@router.put("/templates/{template_id}", response_model=TaskTemplateResponse)
async def update_template(
        template_id: int,
        template_data: TaskTemplateUpdate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Обновление шаблона задачи"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только родители могут обновлять шаблоны задач"
        )

    updated_template = task_crud.update_task_template(db, template_id, template_data)
    if not updated_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Шаблон задачи не найден"
        )
    return updated_template


@router.delete("/templates/{template_id}")
async def delete_template(
        template_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Удаление шаблона задачи"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только родители могут удалять шаблоны задач"
        )

    if not task_crud.delete_task_template(db, template_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Шаблон задачи не найден"
        )
    return {"status": "success"}


# Назначенные задачи

@router.post("/assignments", response_model=TaskAssignmentResponse)
async def create_assignment(
        assignment: TaskAssignmentCreate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Создание нового назначения задачи"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только родители могут назначать задачи"
        )
    return task_crud.create_task_assignment(db, assignment)


@router.get("/assignments", response_model=List[TaskAssignmentResponse])
async def get_assignments(
        child_id: int,
        is_completed: Optional[bool] = None,
        is_approved: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение списка назначенных задач"""
    if current_user.role not in ["parent", "child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен"
        )

    # Для ребенка показываем только его задачи
    if current_user.role == "child" and current_user.id != child_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете видеть только свои задачи"
        )

    return task_crud.get_task_assignments(
        db,
        child_id=child_id,
        is_completed=is_completed,
        is_approved=is_approved,
        skip=skip,
        limit=limit
    )


@router.get("/assignments/{assignment_id}", response_model=TaskAssignmentResponse)
async def get_assignment(
        assignment_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение назначенной задачи по ID"""
    assignment = task_crud.get_task_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )

    # Для ребенка проверяем, что это его задача
    if current_user.role == "child" and current_user.id != assignment.child_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете видеть только свои задачи"
        )

    return assignment


@router.put("/assignments/{assignment_id}", response_model=TaskAssignmentResponse)
async def update_assignment(
        assignment_id: int,
        assignment_data: TaskAssignmentUpdate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Обновление статуса назначенной задачи"""
    assignment = task_crud.get_task_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )

    # Проверяем права доступа
    if current_user.role == "child":
        if current_user.id != assignment.child_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы можете обновлять только свои задачи"
            )
        # Ребенок может только отмечать задачу как выполненную
        if any(field in assignment_data.dict(exclude_unset=True)
               for field in ["is_approved", "approved_at"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Дети не могут одобрять задачи"
            )

    updated_assignment = task_crud.update_task_assignment(
        db, assignment_id, assignment_data
    )
    return updated_assignment