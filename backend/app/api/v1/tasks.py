# app/api/v1/tasks.py
from datetime import datetime  # Добавляем импорт
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

@router.post("/templates/{template_id}/assign", response_model=TaskAssignmentResponse)
async def create_assignment_from_template(
        template_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Создание назначения задачи из шаблона"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только родители могут назначать задачи"
        )

    template = task_crud.get_task_template(db, template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Шаблон задачи не найден"
        )

    # Проверяем, что шаблон активен
    if not template.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Шаблон задачи не активен"
        )

    assignment_data = TaskAssignmentCreate(
        template_id=template_id,
        child_id=template.child_id,
        points_value=template.points_value,  # Добавляем points_value из шаблона
        assigned_at=datetime.utcnow()
    )

    try:
        assignment = task_crud.create_task_assignment(db, assignment_data)
        return assignment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/assignments", response_model=List[TaskAssignmentResponse])
async def get_child_assignments(
        child_id: int,
        is_completed: Optional[bool] = None,
        is_approved: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Получение списка назначенных задач для ребенка"""
    # Проверяем права доступа
    if current_user.role == "child" and current_user.id != child_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете видеть только свои задачи"
        )

    assignments = task_crud.get_task_assignments(
        db,
        child_id=child_id,
        is_completed=is_completed,
        is_approved=is_approved,
        skip=skip,
        limit=limit
    )
    return assignments


@router.put("/assignments/{assignment_id}/complete", response_model=TaskAssignmentResponse)
async def complete_assignment(
        assignment_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Отметка задачи как выполненной (для ребенка)"""
    assignment = task_crud.get_task_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )

    # Проверяем, что это задача текущего ребенка
    if current_user.role == "child" and current_user.id != assignment.child_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете отмечать только свои задачи"
        )

    # Проверяем, не выполнена ли уже задача
    if assignment.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Задача уже отмечена как выполненная"
        )

    update_data = TaskAssignmentUpdate(
        is_completed=True,
        completed_at=datetime.utcnow()
    )

    updated_assignment = task_crud.update_task_assignment(
        db, assignment_id, update_data
    )
    return updated_assignment


@router.put("/assignments/{assignment_id}/approve", response_model=TaskAssignmentResponse)
async def approve_assignment(
        assignment_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Одобрение выполненной задачи (для родителя)"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только родители могут одобрять задачи"
        )

    assignment = task_crud.get_task_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )

    # Проверяем, выполнена ли задача
    if not assignment.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Задача еще не выполнена"
        )

    # Проверяем, не одобрена ли уже задача
    if assignment.is_approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Задача уже одобрена"
        )

    update_data = TaskAssignmentUpdate(
        is_approved=True,
        approved_at=datetime.utcnow()
    )

    updated_assignment = task_crud.update_task_assignment(
        db, assignment_id, update_data
    )
    return updated_assignment