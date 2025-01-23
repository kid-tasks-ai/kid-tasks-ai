# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="parent", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    children = relationship("Child", back_populates="parent")


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer)
    interests = Column(Text)
    preferences = Column(Text)
    points_balance = Column(Integer, default=0)
    role = Column(String, default="child", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    parent = relationship("User", back_populates="children")
    task_templates = relationship("TaskTemplate", back_populates="child")
    task_assignments = relationship("TaskAssignment", back_populates="child")