"""Review endpoints."""

from fastapi import APIRouter, HTTPException, Path, Query
from datetime import datetime

from app.models import Review, ReviewCreate
from app.database import users_db, products_db, reviews_db, next_review_id

router = APIRouter(tags=["reviews"])


@router.post("/products/{product_id}/reviews", response_model=Review, status_code=201, summary="Create product review")
async def create_product_review(
    product_id: int = Path(..., gt=0),
    user_id: int = Query(..., gt=0),
    review: ReviewCreate
):
    """Create a product review (endpoint with validation constraints)."""
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    global next_review_id
    new_review = {
        "id": next_review_id,
        "product_id": product_id,
        "user_id": user_id,
        **review.model_dump(),
        "created_at": datetime.now()
    }
    reviews_db.append(new_review)
    next_review_id += 1
    return new_review