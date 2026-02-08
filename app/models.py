from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    NONE = "none"


class NotificationPreferences(BaseModel):
    order_updates: NotificationType = Field(default=NotificationType.EMAIL)
    promotions: NotificationType = Field(default=NotificationType.EMAIL)


class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")
    created_at: datetime


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="User's full name")
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")