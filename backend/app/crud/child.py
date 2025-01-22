from sqlalchemy.orm import Session
from app.models.user import Child, User
from app.schemas.child import ChildCreate, ChildUpdate
from app.core.security import get_password_hash


def get_user_by_email(db: Session, email: str):
    """Check if email exists in either Users or Children tables"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = db.query(Child).filter(Child.email == email).first()
    return user


def create_child(db: Session, child: ChildCreate, parent_id: int):
    """Create a new child profile"""
    db_child = Child(
        email=child.email,
        password_hash=get_password_hash(child.password),
        name=child.name,
        age=child.age,
        interests=child.interests,
        preferences=child.preferences,
        parent_id=parent_id,
        role="child"
    )
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child


def get_children(db: Session, parent_id: int):
    """Get all children for a parent"""
    return db.query(Child).filter(Child.parent_id == parent_id).all()


def get_child(db: Session, child_id: int, parent_id: int):
    """Get a specific child profile"""
    return db.query(Child).filter(
        Child.id == child_id,
        Child.parent_id == parent_id
    ).first()


def update_child(db: Session, child_id: int, parent_id: int, child_data: ChildUpdate):
    """Update a child profile"""
    db_child = get_child(db, child_id, parent_id)
    if not db_child:
        return None

    update_data = child_data.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(db_child, field, value)

    db.commit()
    db.refresh(db_child)
    return db_child


def delete_child(db: Session, child_id: int, parent_id: int):
    """Delete a child profile"""
    db_child = get_child(db, child_id, parent_id)
    if not db_child:
        return False

    db.delete(db_child)
    db.commit()
    return True