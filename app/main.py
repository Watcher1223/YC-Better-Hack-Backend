"""Main FastAPI application entry point."""

from fastapi import FastAPI
from datetime import datetime

from app.routers import users, products, orders, auth, addresses, reviews, cart, notifications

# Create FastAPI app with metadata
app = FastAPI(
    title="PreMan Demo API",
    description="A demo backend designed to showcase PreMan's capabilities",
    version="1.0.0",
)

# Include routers - PreMan will discover all endpoints from these
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(auth.router)
app.include_router(addresses.router)
app.include_router(reviews.router)
app.include_router(cart.router)
app.include_router(notifications.router)


@app.get("/health", tags=["health"], summary="Health check endpoint")
async def health_check():
    """Health check endpoint for monitoring and testing."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "PreMan Demo API"
    }


@app.get("/", tags=["info"], summary="API information")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "PreMan Demo API",
        "version": "1.0.0",
        "description": "Demo backend for PreMan testing",
        "endpoints": {
            "health": "/health",
            "users": "/users",
            "products": "/products",
            "orders": "/orders",
            "auth": "/auth",
            "addresses": "/users/{user_id}/addresses",
            "reviews": "/products/{product_id}/reviews",
            "cart": "/cart",
            "notifications": "/users/{user_id}/notifications",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }
