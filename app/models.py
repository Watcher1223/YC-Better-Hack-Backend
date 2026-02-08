from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Product(BaseModel):
    """Model for a product."""
    id: int
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    price: float = Field(..., gt=0, description="Product price")
    description: Optional[str] = Field(None, description='Product description')
    in_stock: bool = Field(True, description='Whether product is in stock')

class ProductCreate(BaseModel):
    """Model for creating a product."""
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

class User(BaseModel):
    """Model for a user."""
    id: int
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")
    created_at: datetime

class UserCreate(BaseModel):
    """Model for creating a user."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)

class UserUpdate(BaseModel):
    """Model for updating a user."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)

class OrderResponse(BaseModel):
    """Model for order response."""
    order_id: int
    user_id: int