from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AddSupplier(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    # created_by_id: Optional[int] = None
    # created: Optional[datetime] = None
   

    class Config:
        orm_mode = True
