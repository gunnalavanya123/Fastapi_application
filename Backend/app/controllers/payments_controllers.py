from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db  
from app.services.payments_service import get_payment , get_all_payments  

router = APIRouter()

@router.get("/payments/{payment_id}")
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    return get_payment(db, payment_id)


@router.get("/payments/")
def read_all_payments(db: Session = Depends(get_db)):
    return get_all_payments(db)
