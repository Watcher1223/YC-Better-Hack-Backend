"""Product endpoints."""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional

from app.models import Product, ProductCreate
from app.database import products_db, next_product_id

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=List[Product], summary="List all products")
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    in_stock: Optional[bool] = Query(None)
):
    """List products with filtering."""
    result = products_db[skip:skip+limit]
    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]
    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
    if in_stock is not None:
        result = [p for p in result if p["in_stock"] == in_stock]
    return result


@router.get("/{product_id}", response_model=Product, summary="Get product by ID")
async def get_product(
    product_id: int = Path(..., gt=0)
):
    """Get a specific product by ID."""
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


@router.post("", response_model=Product, status_code=201, summary="Create a new product")
async def create_product(product: ProductCreate):
    """Create a new product."""
    global next_product_id
    new_product = {
        "id": next_product_id,
        **product.model_dump()
    }
    products_db.append(new_product)
    next_product_id += 1
    return new_product