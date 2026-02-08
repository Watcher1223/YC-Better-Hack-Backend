from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"
    NONE = "none"


class NotificationPreferences(BaseModel):
    order_updates: NotificationType = Field(default=NotificationType.EMAIL)
    promotions: NotificationType = Field(default=NotificationType.EMAIL)
    shipping_updates: NotificationType = Field(default=NotificationType.SMS)
    marketing: NotificationType = Field(default=NotificationType.NONE)


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)


class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")
    created_at: datetime


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)