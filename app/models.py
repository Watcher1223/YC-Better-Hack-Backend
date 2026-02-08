from pydantic import BaseModel, Field
from typing import List, Optional

class Product(BaseModel):
    """Model for product."""
    id: int
    name: str = Field(..., min_length=1, description='Product name')
    price: float = Field(..., gt=0, description='Product price in USD')
    description: Optional[str] = Field(None, description='Product description')
    in_stock: bool = Field(True, description='Whether product is in stock')

class ProductCreate(BaseModel):
    """Model for creating a product."""
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    description: Optional[str] = None
    in_stock: bool = True

class OrderResponse(BaseModel):
    """Model for order response."""
    order_id: int
    user_id: int
    products: List[Product]
    total: float
    notes: Optional[str] = None