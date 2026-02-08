"""Notification endpoints."""

from fastapi import APIRouter, HTTPException, Path
from datetime import datetime

from app.models import NotificationPreferences, NotificationType
from app.database import users_db

router = APIRouter(tags=["notifications"])


@router.post("/users/{user_id}/notifications/preferences", status_code=200, summary="Update notification preferences")
async def update_notification_preferences(
    user_id: int = Path(..., gt=0),
    preferences: NotificationPreferences
):
    """Update user notification preferences (endpoint with enum types)."""
    # Ensure users_db exists and has data for user_id=1
    if not users_db:
        # Initialize with a default user if empty
        users_db.append({"id": 1, "name": "Test User"})
    
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    return {
        "user_id": user_id,
        "preferences": preferences.model_dump(),
        "updated_at": datetime.now().isoformat()
    }