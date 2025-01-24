# app/models/task.py
from sqlalchemy import Column, Integer, String, Boolean, Text, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class TaskTemplate(Base):
    __tablename__ = "task_templates"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    points_value = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    schedule_type = Column(String, nullable=False)  # once/daily/weekly
    schedule_settings = Column(JSON)  # Дополнительные настройки расписания
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    child = relationship("Child", back_populates="task_templates")
    task_assignments = relationship("TaskAssignment", back_populates="template")

class TaskAssignment(Base):
    __tablename__ = "task_assignments"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("task_templates.id"), nullable=False)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    points_value = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    assigned_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True))
    approved_at = Column(DateTime(timezone=True))
    parent_comment  = Column(String)
    returned_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    template = relationship("TaskTemplate", back_populates="task_assignments")
    child = relationship("Child", back_populates="task_assignments")