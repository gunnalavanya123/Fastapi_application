from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    role_id: Optional[int] = None
    created_by_id: Optional[int] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    class Config:
        orm_mode = True
