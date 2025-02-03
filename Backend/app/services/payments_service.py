from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.model.payments import Payments
from app.model.plans import Plan
from sqlalchemy.exc import SQLAlchemyError

def get_payment(db: Session, payment_id: int) -> dict:
    try:
        # Fetch the payment record
        db_payment = db.query(Payments).filter(Payments.payment_id == payment_id).first()
        if db_payment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
        
        # Fetch the related plan data
        db_plan = db.query(Plan).filter(Plan.plan_id == db_payment.plan_id).first()

        # Prepare the response data
        response = {
            "payment_id": db_payment.payment_id,
            "orgId": db_payment.orgId,
            "date": db_payment.date,
            "amount": db_payment.amount,
            "pay_status": db_payment.pay_status,
            "plan_id": db_payment.plan_id,
        }
        
        return response 
    except SQLAlchemyError as e:
        # Handle SQLAlchemy-related errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {str(e)}")
    
def get_all_payments(db: Session) -> list:
    try:
        # Fetch all payment records
        db_payments = db.query(Payments).all()

        # Prepare the response data
        response = [
            {
                "payment_id": payment.payment_id,
                "orgId": payment.orgId,
                "date": payment.date,
                "amount": payment.amount,
                "pay_status": payment.pay_status,
                "plan_id": payment.plan_id,
            }
            for payment in db_payments
        ]
        
        return response 
    except SQLAlchemyError as e:
        # Handle SQLAlchemy-related errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {str(e)}")

