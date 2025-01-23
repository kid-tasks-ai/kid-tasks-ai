from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.task import TaskTemplate, TaskAssignment
from app.schemas.task import TaskTemplateCreate, TaskTemplateUpdate, TaskAssignmentCreate, TaskAssignmentUpdate


def create_task_template(db: Session, template: TaskTemplateCreate) -> TaskTemplate:
    db_template = TaskTemplate(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


def get_task_template(db: Session, template_id: int) -> Optional[TaskTemplate]:
    return db.query(TaskTemplate).filter(TaskTemplate.id == template_id).first()


def get_task_templates(
        db: Session,
        child_id: int,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        category: Optional[str] = None
) -> List[TaskTemplate]:
    query = db.query(TaskTemplate).filter(TaskTemplate.child_id == child_id)

    if is_active is not None:
        query = query.filter(TaskTemplate.is_active == is_active)

    if category:
        query = query.filter(TaskTemplate.category == category)

    return query.offset(skip).limit(limit).all()


def update_task_template(
        db: Session, template_id: int, template_data: TaskTemplateUpdate
) -> Optional[TaskTemplate]:
    template = get_task_template(db, template_id)
    if not template:
        return None

    for field, value in template_data.model_dump(exclude_unset=True).items():
        setattr(template, field, value)

    db.commit()
    db.refresh(template)
    return template


def delete_task_template(db: Session, template_id: int) -> bool:
    template = get_task_template(db, template_id)
    if not template:
        return False

    db.delete(template)
    db.commit()
    return True


def create_task_assignment(db: Session, assignment: TaskAssignmentCreate) -> TaskAssignment:
    """Создание нового назначения задачи из шаблона"""
    # Получаем шаблон
    template = db.query(TaskTemplate).filter(TaskTemplate.id == assignment.template_id).first()
    if not template:
        raise ValueError("Шаблон задачи не найден")

    # Создаем назначение
    db_assignment = TaskAssignment(
        template_id=assignment.template_id,
        child_id=assignment.child_id,
        points_value=template.points_value,
        assigned_at=assignment.assigned_at
    )

    # Деактивируем шаблон, если он одноразовый
    if template.schedule_type == 'once':
        template.is_active = False

    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


def get_task_assignments(
        db: Session,
        child_id: int,
        is_completed: Optional[bool] = None,
        is_approved: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
) -> List[TaskAssignment]:
    """Получение списка назначенных задач с фильтрацией"""
    query = db.query(TaskAssignment).filter(TaskAssignment.child_id == child_id)

    if is_completed is not None:
        query = query.filter(TaskAssignment.is_completed == is_completed)
    if is_approved is not None:
        query = query.filter(TaskAssignment.is_approved == is_approved)

    return query.offset(skip).limit(limit).all()


def get_task_assignment(db: Session, assignment_id: int) -> Optional[TaskAssignment]:
    """Получение назначенной задачи по ID"""
    return db.query(TaskAssignment).filter(TaskAssignment.id == assignment_id).first()


def update_task_assignment(
        db: Session,
        assignment_id: int,
        assignment_data: TaskAssignmentUpdate
) -> Optional[TaskAssignment]:
    """Обновление статуса назначенной задачи"""
    db_assignment = get_task_assignment(db, assignment_id)
    if not db_assignment:
        return None

    update_data = assignment_data.dict(exclude_unset=True)

    # Если задача отмечается как выполненная, добавляем дату выполнения
    if update_data.get('is_completed') and not db_assignment.completed_at:
        update_data['completed_at'] = datetime.utcnow()

    # Если задача одобряется, добавляем дату одобрения
    if update_data.get('is_approved') and not db_assignment.approved_at:
        update_data['approved_at'] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(db_assignment, field, value)

    db.commit()
    db.refresh(db_assignment)
    return db_assignment


def get_pending_assignments(db: Session, child_id: int) -> List[TaskAssignment]:
    """Получение списка невыполненных задач"""
    return db.query(TaskAssignment).filter(
        and_(
            TaskAssignment.child_id == child_id,
            TaskAssignment.is_completed == False
        )
    ).all()


def get_completed_assignments(db: Session, child_id: int) -> List[TaskAssignment]:
    """Получение списка выполненных, но не одобренных задач"""
    return db.query(TaskAssignment).filter(
        and_(
            TaskAssignment.child_id == child_id,
            TaskAssignment.is_completed == True,
            TaskAssignment.is_approved == False
        )
    ).all()


def delete_task_assignment(db: Session, assignment_id: int) -> bool:
    """Удаление назначенной задачи"""
    db_assignment = get_task_assignment(db, assignment_id)
    if not db_assignment:
        return False

    db.delete(db_assignment)
    db.commit()
    return True