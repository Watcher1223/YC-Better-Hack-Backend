"""Database module for storing user data."""

from datetime import datetime

# In-memory database for users
users_db = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "created_at": datetime(2023, 1, 1, 12, 0, 0)
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "age": 25,
        "created_at": datetime(2023, 1, 2, 12, 0, 0)
    }
]

# Counter for generating new user IDs
next_user_id = 3