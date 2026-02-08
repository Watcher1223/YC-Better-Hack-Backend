from enum import Enum
from pydantic import BaseModel, Field

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