from sqlalchemy.orm import Session
from app.models.user import Child
from app.schemas.child import ChildCreate, ChildUpdate
from app.core.security import get_password_hash


def create_child(db: Session, child: ChildCreate, parent_id: int):
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
    return db.query(Child).filter(Child.parent_id == parent_id).all()


def get_child(db: Session, child_id: int, parent_id: int):
    return db.query(Child).filter(
        Child.id == child_id,
        Child.parent_id == parent_id
    ).first()


def update_child(db: Session, child_id: int, parent_id: int, child_data: ChildUpdate):
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
    db_child = get_child(db, child_id, parent_id)
    if not db_child:
        return False

    db.delete(db_child)
    db.commit()
    return True