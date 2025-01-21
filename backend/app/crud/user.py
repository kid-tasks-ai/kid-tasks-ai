# app/crud/user.py
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.models.user import User, Child
from app.schemas.user import UserCreate

def get_user(db: Session, user_id: int):
    """Get user by ID from either Users or Children table"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = db.query(Child).filter(Child.id == user_id).first()
    return user

def get_user_by_email(db: Session, email: str):
    """Get user by email from either Users or Children table"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = db.query(Child).filter(Child.email == email).first()
    return user

def create_user(db: Session, user: UserCreate):
    """Create a new parent user"""
    db_user = User(
        email=user.email,
        name=user.name,
        password_hash=get_password_hash(user.password),
        role="parent"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate(db: Session, *, email: str, password: str):
    """Authenticate user by email and password"""
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user