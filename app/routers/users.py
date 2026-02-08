"""User endpoints."""

from fastapi import APIRouter, HTTPException, Query, Path, Response
from typing import List, Optional
from datetime import datetime

from app.models import User, UserCreate, UserUpdate
from app.database import users_db, next_user_id

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[User], summary="List all users")
async def list_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of users to return"),
    search: Optional[str] = Query(None, description="Search users by name")
):
    """List all users with pagination and search."""
    result = users_db[skip:skip+limit]
    if search:
        result = [u for u in result if search.lower() in u["name"].lower()]
    return result


@router.get("/{user_id}", response_model=User, summary="Get user by ID")
async def get_user(
    user_id: int = Path(..., description="User ID", gt=0)
):
    """Get a specific user by ID."""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


@router.post("/", response_model=User, status_code=201, summary="Create a new user")
async def create_user(user: UserCreate):
    """Create a new user."""
    global next_user_id
    new_user = User(
        id=next_user_id,
        **user.model_dump(),
        created_at=datetime.now()
    )
    users_db.append(new_user.model_dump())
    next_user_id += 1
    return new_user


@router.put("/{user_id}", response_model=User, summary="Update user")
async def update_user(
    user_id: int = Path(..., description="User ID", gt=0),
    user_update: UserUpdate = ...
):
    """Update an existing user."""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    user.update(update_data)
    return user


@router.delete("/{user_id}", status_code=204, summary="Delete user")
async def delete_user(
    user_id: int = Path(..., description="User ID", gt=0)
):
    """Delete a user."""
    global users_db
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    users_db = [u for u in users_db if u["id"] != user_id]
    return Response(status_code=204)