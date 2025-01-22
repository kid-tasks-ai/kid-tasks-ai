from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.child import ChildCreate, ChildUpdate, ChildResponse
from app.crud import child as child_crud
from app.schemas.user import UserResponse

router = APIRouter()


@router.post("", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
async def create_child_profile(
        child_data: ChildCreate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Create a new child profile"""
    # Check if user is a parent
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can create child profiles"
        )

    try:
        # Check if email is already registered
        existing_user = child_crud.get_user_by_email(db, email=child_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )

        # Create child profile
        child = child_crud.create_child(db, child_data, current_user.id)
        return child
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("", response_model=List[ChildResponse])
async def get_children_profiles(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Get all child profiles for the current parent"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to parents"
        )

    try:
        return child_crud.get_children(db, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{child_id}", response_model=ChildResponse)
async def get_child_profile(
        child_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Get a specific child profile"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to parents"
        )

    child = child_crud.get_child(db, child_id, current_user.id)
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )

    return child


@router.put("/{child_id}", response_model=ChildResponse)
async def update_child_profile(
        child_id: int,
        child_data: ChildUpdate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Update a child profile"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to parents"
        )

    try:
        updated_child = child_crud.update_child(
            db, child_id, current_user.id, child_data
        )
        if not updated_child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Child profile not found"
            )
        return updated_child
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{child_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_child_profile(
        child_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """Delete a child profile"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to parents"
        )

    try:
        success = child_crud.delete_child(db, child_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Child profile not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )