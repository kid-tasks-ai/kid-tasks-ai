from pydantic import BaseModel, EmailStr
from typing import Optional

class ChildBase(BaseModel):
    name: str
    email: EmailStr
    age: int
    gender: Optional[str] = None
    interests: Optional[str] = None
    preferences: Optional[str] = None

class ChildCreate(ChildBase):
    password: str

class ChildUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    interests: Optional[str] = None
    preferences: Optional[str] = None
    password: Optional[str] = None

class ChildResponse(ChildBase):
    id: int
    parent_id: int
    points_balance: int
    role: str = "child"

    class Config:
        from_attributes = True