from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class OrderItem(BaseModel):
    """Model for order item."""
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity")

class AddressCreate(BaseModel):
    """Model for creating an address."""
    street: str = Field(..., max_length=200, description="Street address")
    city: str = Field(..., max_length=100, description="City")
    state: str = Field(..., max_length=50, description="State")
    zip_code: str = Field(..., max_length=20, description="ZIP code")
    country: str = Field(..., max_length=50, description="Country")

class Product(BaseModel):
    """Model for product."""
    id: int
    name: str
    price: float
    description: Optional[str] = None

class OrderCreate(BaseModel):
    """Model for creating an order (with nested OrderItem list)."""
    user_id: int = Field(..., gt=0, description="User ID placing the order")
    items: List[OrderItem] = Field(..., min_length=1, max_length=50, description="List of order items")
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