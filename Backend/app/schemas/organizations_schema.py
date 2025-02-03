from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class OrganizationCreate(BaseModel):
    organization_iD: Optional[str] = None
    org_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    created_by_id: Optional[int] = None
    created: Optional[datetime] = None


class OrganizationUpdate(BaseModel):
    organization_iD: Optional[str] = None
    org_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    updated_by_id: Optional[int] = None
    updated: Optional[datetime] = None

    class Config:
        orm_mode = True

class StatusUpdate(BaseModel):
    status: Optional[int] = None
    updated_by_id: Optional[int] = None
    updated:  Optional[datetime] = None


    class Config:
        orm_mode = True
