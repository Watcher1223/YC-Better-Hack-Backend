"""Entry point to run the FastAPI application."""

try:
    import uvicorn  # type: ignore
except ImportError:
    raise ImportError("uvicorn is not installed. Run: pip install uvicorn[standard]")

from app.main import app

# Export app for uvicorn/gunicorn when called as "main:app"
__all__ = ["app"]

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )
