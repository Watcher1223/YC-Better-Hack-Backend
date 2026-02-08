from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    description: Optional[str] = Field(None)
    in_stock: bool = Field(True)

class Product(BaseModel):
    id: int
    name: str = Field(..., min_length=1, description='Product name')
    price: float = Field(..., gt=0, description='Product price in USD')
    description: Optional[str] = Field(None, description='Product description')
    in_stock: bool = Field(True, description='Whether product is in stock')