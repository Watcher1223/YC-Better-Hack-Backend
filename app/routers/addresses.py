"""Address endpoints."""

from fastapi import APIRouter, HTTPException, Path

from app.models import Address, AddressCreate
from app.database import users_db, addresses_db, next_address_id

router = APIRouter(tags=["addresses"])


@router.post("/users/{user_id}/addresses", response_model=Address, status_code=201, summary="Add address for user")
async def create_user_address(
    user_id: int = Path(..., gt=0),
    address: AddressCreate
):
    """Add an address for a user (nested model endpoint)."""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    global next_address_id
    new_address = {
        "id": next_address_id,
        "user_id": user_id,
        **address.model_dump()
    }
    addresses_db.append(new_address)
    next_address_id += 1
    return new_address