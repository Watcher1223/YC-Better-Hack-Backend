"""Authentication endpoints."""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.models import User, LoginRequest, RegisterRequest
from app.database import users_db

router = APIRouter(prefix="/auth", tags=["auth"])

next_user_id = 1


@router.post("/login", status_code=200, summary="Login")
async def login(credentials: LoginRequest):
    """Authenticate a user (endpoint with password field)."""
    # Demo: Check if user exists (in real app, verify password hash)
    user = next((u for u in users_db if u["email"] == credentials.email), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "access_token": f"demo_token_{user['id']}",
        "token_type": "bearer",
        "user_id": user["id"],
        "expires_in": 3600
    }


@router.post("/register", response_model=User, status_code=201, summary="Register a new user")
async def register(user_data: RegisterRequest):
    """Register a new user (endpoint with password confirmation)."""
    # Validate password match
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Check if email already exists
    if any(u["email"] == user_data.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    global next_user_id
    new_user = {
        "id": next_user_id,
        "name": user_data.name,
        "email": user_data.email,
        "age": user_data.age,
        "created_at": datetime.now()
    }
    users_db.append(new_user)
    next_user_id += 1
    return new_user