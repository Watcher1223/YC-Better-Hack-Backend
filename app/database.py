"""In-memory database for demo purposes."""

from typing import Dict, List

# In-memory storage
users_db: List[Dict] = []
products_db: List[Dict] = []
addresses_db: List[Dict] = []
reviews_db: List[Dict] = []
carts_db: List[Dict] = []

# ID counters
next_user_id = 1
next_product_id = 1
next_address_id = 1
next_review_id = 1
next_cart_id = 1


def get_user_by_id(user_id: int) -> Dict | None:
    """Get a user by ID from the in-memory database."""
    return next((u for u in users_db if u["id"] == user_id), None)


def get_product_by_id(product_id: int) -> Dict | None:
    """Get a product by ID from the in-memory database."""
    return next((p for p in products_db if p["id"] == product_id), None)
