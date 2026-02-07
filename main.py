from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

app = FastAPI(
    title="PreMan Demo API",
    description="A demo backend to showcase PreMan's capabilities",
    version="1.0.0"
)

# ─── Pydantic Models ────────────────────────────────────────────────

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)
    created_at: datetime

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)

class Product(BaseModel):
    id: int
    name: str
    price: float = Field(..., gt=0)
    description: Optional[str] = None
    in_stock: bool = True

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    description: Optional[str] = None
    in_stock: bool = True

class Address(BaseModel):
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)
    zip_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')
    country: str = Field(default="USA", min_length=2, max_length=100)

class AddressCreate(BaseModel):
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)
    zip_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')
    country: str = Field(default="USA", min_length=2, max_length=100)
    is_primary: bool = Field(default=False)

class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    title: str = Field(..., min_length=1, max_length=200)
    comment: str = Field(..., min_length=10, max_length=2000)
    verified_purchase: bool = Field(default=False)

class Review(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    title: str
    comment: str
    verified_purchase: bool
    created_at: datetime

class CartItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=100)

class CartCreate(BaseModel):
    items: List[CartItem] = Field(..., min_items=1, max_items=50)
    coupon_code: Optional[str] = Field(None, max_length=20)

class Cart(BaseModel):
    cart_id: int
    user_id: Optional[int] = None
    items: List[dict]
    total: float
    coupon_code: Optional[str] = None
    created_at: datetime

class LoginRequest(BaseModel):
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=8, max_length=100)

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=8, max_length=100, description="Password must be at least 8 characters")
    confirm_password: str = Field(..., min_length=8, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)

class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    NONE = "none"

class NotificationPreferences(BaseModel):
    order_updates: NotificationType = Field(default=NotificationType.EMAIL)
    promotions: NotificationType = Field(default=NotificationType.EMAIL)
    shipping_updates: NotificationType = Field(default=NotificationType.SMS)
    marketing: NotificationType = Field(default=NotificationType.NONE)

# ─── In-Memory Database (for demo) ──────────────────────────────────

users_db = []
products_db = []
addresses_db = []
reviews_db = []
carts_db = []
next_user_id = 1
next_product_id = 1
next_address_id = 1
next_review_id = 1
next_cart_id = 1

# ─── Health Check ───────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ─── User Endpoints ─────────────────────────────────────────────────

@app.get("/users", response_model=List[User])
async def list_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of users to return"),
    search: Optional[str] = Query(None, description="Search users by name")
):
    """List all users with pagination and search."""
    result = users_db[skip:skip+limit]
    if search:
        result = [u for u in result if search.lower() in u["name"].lower()]
    return result

@app.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: int = Path(..., description="User ID", gt=0)
):
    """Get a specific user by ID."""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user

@app.post("/users", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    """Create a new user."""
    global next_user_id
    new_user = {
        "id": next_user_id,
        **user.model_dump(),
        "created_at": datetime.now()
    }
    users_db.append(new_user)
    next_user_id += 1
    return new_user

@app.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: int = Path(..., description="User ID", gt=0),
    user_update: UserUpdate = ...
):
    """Update an existing user."""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    user.update(update_data)
    return user

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int = Path(..., description="User ID", gt=0)
):
    """Delete a user."""
    global users_db
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    users_db = [u for u in users_db if u["id"] != user_id]
    return None

# ─── Product Endpoints ──────────────────────────────────────────────

@app.get("/products", response_model=List[Product])
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

@app.get("/products/{product_id}", response_model=Product)
async def get_product(
    product_id: int = Path(..., gt=0)
):
    """Get a specific product by ID."""
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product

@app.post("/products", response_model=Product, status_code=201)
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

# ─── Complex Endpoint (to showcase schema extraction) ────────────────

@app.post("/orders", status_code=201)
async def create_order(
    user_id: int = Query(..., gt=0),
    product_ids: List[int] = Query(..., min_items=1),
    notes: Optional[str] = None
):
    """Create an order (complex endpoint with multiple parameters)."""
    # Validate user exists
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    # Validate products exist
    products = [p for p in products_db if p["id"] in product_ids]
    if len(products) != len(product_ids):
        missing = set(product_ids) - {p["id"] for p in products}
        raise HTTPException(status_code=404, detail=f"Products not found: {missing}")
    
    total = sum(p["price"] for p in products)
    return {
        "order_id": len(products_db) + 1,
        "user_id": user_id,
        "products": products,
        "total": total,
        "notes": notes,
        "created_at": datetime.now().isoformat()
    }

# ─── Additional POST Endpoints (to showcase schema extraction) ───────

@app.post("/users/{user_id}/addresses", response_model=Address, status_code=201)
async def create_user_address(
    user_id: int = Path(..., gt=0),
    address: AddressCreate = ...
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

@app.post("/products/{product_id}/reviews", response_model=Review, status_code=201)
async def create_product_review(
    product_id: int = Path(..., gt=0),
    user_id: int = Query(..., gt=0),
    review: ReviewCreate = ...
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

@app.post("/cart", response_model=Cart, status_code=201)
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

@app.post("/auth/login", status_code=200)
async def login(credentials: LoginRequest):
    """Authenticate a user (endpoint with password field)."""
    # Demo: Check if user exists (in real app, verify password hash)
    user = next((u for u in users_db if u["email"] == credentials.email), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "access_token": f"demo_token_{user['id']}",
        "token_type": "bearer",
        "user_id": user["id"],
        "expires_in": 3600
    }

@app.post("/auth/register", response_model=User, status_code=201)
async def register(user_data: RegisterRequest):
    """Register a new user (endpoint with password confirmation)."""
    # Validate password match
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Check if email already exists
    if any(u["email"] == user_data.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    global next_user_id
    new_user = {
        "id": next_user_id,
        "name": user_data.name,
        "email": user_data.email,
        "age": user_data.age,
        "created_at": datetime.now()
    }
    users_db.append(new_user)
    next_user_id += 1
    return new_user

@app.post("/users/{user_id}/notifications/preferences", status_code=200)
async def update_notification_preferences(
    user_id: int = Path(..., gt=0),
    preferences: NotificationPreferences = ...
):
    """Update user notification preferences (endpoint with enum types)."""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    return {
        "user_id": user_id,
        "preferences": preferences.model_dump(),
        "updated_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
