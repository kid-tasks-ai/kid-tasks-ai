from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.task import TaskTemplateBase


class TaskGenerationRequest(BaseModel):
    child_id: int
    task_count: int = Field(ge=1, le=10)
    description: str
class ChildDescription(BaseModel):
    age: int
    interests: Optional[str] = None
    gender: Optional[str] = None

class TaskGenerationPayload(BaseModel):
    child_description: ChildDescription
    tasks_description: dict = Field(
        default_factory=lambda: {
            "creative_tasks": {"amount": 1, "topics": []}
        }
    )


class TaskGenerationResponse(BaseModel):
    tasks: List[TaskTemplateBase]
    error: Optional[str] = None

