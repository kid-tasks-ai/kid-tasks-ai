# app/schemas/task.py
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class TaskTemplateBase(BaseModel):
    title: str
    description: str
    points_value: int = Field(ge=0)
    schedule_type: str = Field(pattern="^(once|daily|weekly)$")
    schedule_settings: Optional[Dict[str, Any]] = None

class TaskTemplateCreate(TaskTemplateBase):
    child_id: int

class TaskTemplateUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    points_value: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    schedule_type: Optional[str] = Field(None, pattern="^(once|daily|weekly)$")
    schedule_settings: Optional[Dict[str, Any]] = None

class TaskTemplateResponse(TaskTemplateBase):
    id: int
    child_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskAssignmentBase(BaseModel):
    points_value: int

class TaskAssignmentCreate(TaskAssignmentBase):
    template_id: int
    child_id: int
    assigned_at: datetime

class TaskAssignmentUpdate(BaseModel):
    is_completed: Optional[bool] = None
    is_approved: Optional[bool] = None
    parent_comment: Optional[str] = None
    completed_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None

class TaskAssignmentResponse(TaskAssignmentBase):
    id: int
    template_id: int
    child_id: int
    is_completed: bool
    is_approved: bool
    assigned_at: datetime
    completed_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    parent_comment: Optional[str] = None
    returned_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    template: TaskTemplateResponse

    class Config:
        from_attributes = True