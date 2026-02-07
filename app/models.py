"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class User(BaseModel):
    """User model with validation rules."""
    id: int
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")
    created_at: datetime


class UserCreate(BaseModel):
    """Model for creating a new user."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)


class UserUpdate(BaseModel):
    """Model for updating an existing user."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)


class Product(BaseModel):
    """Product model."""
    id: int
    name: str = Field(..., min_length=1, description="Product name")
    price: float = Field(..., gt=0, description="Product price in USD")
    description: Optional[str] = Field(None, description="Product description")
    in_stock: bool = Field(True, description="Whether product is in stock")


class ProductCreate(BaseModel):
    """Model for creating a new product."""
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    description: Optional[str] = None
    in_stock: bool = True


class Address(BaseModel):
    """Address model."""
    id: int
    user_id: int
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)
    zip_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')
    country: str = Field(default="USA", min_length=2, max_length=100)
    is_primary: bool = Field(default=False)


class AddressCreate(BaseModel):
    """Model for creating a new address."""
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)
    zip_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')
    country: str = Field(default="USA", min_length=2, max_length=100)
    is_primary: bool = Field(default=False)


class ReviewCreate(BaseModel):
    """Model for creating a product review."""
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    title: str = Field(..., min_length=1, max_length=200)
    comment: str = Field(..., min_length=10, max_length=2000)
    verified_purchase: bool = Field(default=False)


class Review(BaseModel):
    """Review model."""
    id: int
    product_id: int
    user_id: int
    rating: int
    title: str
    comment: str
    verified_purchase: bool
    created_at: datetime


class CartItem(BaseModel):
    """Cart item model."""
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=100)


class CartCreate(BaseModel):
    """Model for creating a shopping cart."""
    items: List[CartItem] = Field(..., min_items=1, max_items=50)
    coupon_code: Optional[str] = Field(None, max_length=20)


class Cart(BaseModel):
    """Cart model."""
    cart_id: int
    user_id: Optional[int] = None
    items: List[dict]
    total: float
    coupon_code: Optional[str] = None
    created_at: datetime


class LoginRequest(BaseModel):
    """Model for login request."""
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=8, max_length=100)


class RegisterRequest(BaseModel):
    """Model for user registration."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=8, max_length=100, description="Password must be at least 8 characters")
    confirm_password: str = Field(..., min_length=8, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)


class NotificationType(str, Enum):
    """Notification type enum."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    NONE = "none"


class NotificationPreferences(BaseModel):
    """Model for notification preferences."""
    order_updates: NotificationType = Field(default=NotificationType.EMAIL)
    promotions: NotificationType = Field(default=NotificationType.EMAIL)
    shipping_updates: NotificationType = Field(default=NotificationType.SMS)
    marketing: NotificationType = Field(default=NotificationType.NONE)


class OrderItem(BaseModel):
    """Order item model (nested in OrderCreate)."""
    product_id: int = Field(..., gt=0, description="Product ID to order")
    quantity: int = Field(..., ge=1, le=100, description="Quantity of product")
    special_instructions: Optional[str] = Field(None, max_length=500, description="Special instructions for this item")


class OrderCreate(BaseModel):
    """Model for creating an order (with nested OrderItem list)."""
    user_id: int = Field(..., gt=0, description="User ID placing the order")
    items: List[OrderItem] = Field(..., min_items=1, max_items=50, description="List of order items")
    shipping_address: Optional[AddressCreate] = Field(None, description="Shipping address (nested model)")
    notes: Optional[str] = Field(None, max_length=1000, description="Order notes")
    payment_method: Optional[str] = Field(None, max_length=50, description="Payment method")


class OrderResponse(BaseModel):
    """Model for order response."""
    order_id: int
    user_id: int
    products: List[Product]
    total: float
    notes: Optional[str] = None
    created_at: str
