from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CartItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class CartCreate(BaseModel):
    items: List[CartItem] = Field(..., min_length=1, max_length=50)
    coupon_code: Optional[str] = Field(None, max_length=20)

class Cart(BaseModel):
    cart_id: int
    user_id: Optional[int] = None
    items: List[dict]
    total: float
    coupon_code: Optional[str] = None
    created_at: datetime