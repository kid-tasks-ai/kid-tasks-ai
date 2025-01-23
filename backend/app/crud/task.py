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
    db_assignment = TaskAssignment(**assignment.model_dump())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


def get_task_assignment(db: Session, assignment_id: int) -> Optional[TaskAssignment]:
    return db.query(TaskAssignment).filter(TaskAssignment.id == assignment_id).first()


def get_task_assignments(
        db: Session,
        child_id: int,
        skip: int = 0,
        limit: int = 100,
        is_completed: Optional[bool] = None,
        is_approved: Optional[bool] = None
) -> List[TaskAssignment]:
    query = db.query(TaskAssignment).filter(TaskAssignment.child_id == child_id)

    if is_completed is not None:
        query = query.filter(TaskAssignment.is_completed == is_completed)

    if is_approved is not None:
        query = query.filter(TaskAssignment.is_approved == is_approved)

    return query.offset(skip).limit(limit).all()


def update_task_assignment(
        db: Session, assignment_id: int, assignment_data: TaskAssignmentUpdate
) -> Optional[TaskAssignment]:
    assignment = get_task_assignment(db, assignment_id)
    if not assignment:
        return None

    for field, value in assignment_data.model_dump(exclude_unset=True).items():
        setattr(assignment, field, value)

    db.commit()
    db.refresh(assignment)
    return assignment