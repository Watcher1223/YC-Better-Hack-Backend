"""Cart endpoints."""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

from app.models import Cart, CartCreate
from app.database import products_db, carts_db, next_cart_id

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("", response_model=Cart, status_code=201, summary="Create shopping cart")
async def create_cart(
    cart: CartCreate,
    user_id: Optional[int] = Query(None, gt=0)
):
    """Create a shopping cart (endpoint with nested list models)."""
    # Validate all products exist
    product_ids = [item.product_id for item in cart.items]
    products = {p["id"]: p for p in products_db if p["id"] in product_ids}
    
    if len(products) != len(product_ids):
        missing = set(product_ids) - set(products.keys())
        raise HTTPException(status_code=404, detail=f"Products not found: {missing}")
    
    # Calculate total
    cart_items = []
    total = 0.0
    for item in cart.items:
        product = products[item.product_id]
        item_total = product["price"] * item.quantity
        total += item_total
        cart_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": product["price"],
            "subtotal": item_total
        })
    
    global next_cart_id
    new_cart = {
        "cart_id": next_cart_id,
        "user_id": user_id,
        "items": cart_items,
        "total": round(total, 2),
        "coupon_code": cart.coupon_code,
        "created_at": datetime.now()
    }
    carts_db.append(new_cart)
    next_cart_id += 1
    return new_cart