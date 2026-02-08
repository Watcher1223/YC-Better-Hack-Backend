"""Order endpoints."""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.models import OrderCreate, OrderResponse, Product
from app.database import users_db, products_db

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=201, summary="Create an order")
async def create_order(order: OrderCreate):
    """Create an order (complex endpoint with nested body schema - OrderItem list and Address)."""
    # Validate user exists
    user = next((u for u in users_db if u["id"] == order.user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {order.user_id} not found")
    
    # Validate products exist and calculate totals
    products = []
    total = 0.0
    
    for item in order.items:
        product = next((p for p in products_db if p["id"] == item.productId), None)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.productId} not found")
        
        products.append(product)
        total += product["price"] * item.quantity
    
    return OrderResponse(
        order_id=len(products_db) + 1,
        user_id=order.user_id,
        products=products,
        total=round(total, 2),
        notes=order.notes,
        created_at=datetime.now().isoformat()
    )