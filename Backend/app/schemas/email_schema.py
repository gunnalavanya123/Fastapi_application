from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str