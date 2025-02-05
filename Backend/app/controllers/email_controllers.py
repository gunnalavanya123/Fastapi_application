from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from app.db.database import get_db
# from app.model.suppliers import Supplier
# from app.schemas.supplier_schema import AddSupplier
from app.services.email_service import EmailService
from app.schemas.email_schema import EmailRequest
from typing import List,Optional,Dict

router = APIRouter()

email_service = EmailService()

@router.post("/send-email/")
async def send_email(email: EmailRequest):
    try:
        # Call the send_email method from EmailService
        result = email_service.send_email(email.to_email, email.subject, email.body)
        return {"message": result}  # Return success message
    except Exception as e:
        # Handle errors by raising an HTTPException
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")