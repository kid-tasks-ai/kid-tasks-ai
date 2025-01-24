from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class RewardBase(BaseModel):
    name: str
    description: Optional[str] = None
    points_cost: int = Field(gt=0, description="Стоимость награды в баллах")

class RewardCreate(RewardBase):
    child_id: int

class RewardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    points_cost: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None
    is_redeemed: Optional[bool] = None

class RewardResponse(RewardBase):
    id: int
    child_id: int
    is_active: bool
    is_redeemed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    redeemed_at: Optional[datetime] = None

    class Config:
        from_attributes = True