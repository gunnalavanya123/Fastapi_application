from fastapi import HTTPException,status
from app.db.database import get_db
from sqlalchemy import func,desc,asc
from app.model.miscellaneous import Miscellaneous
from app.model.user import User
from sqlalchemy.orm import Session
from app.model.suppliers import Supplier
from app.schemas.supplier_schema import AddSupplier
from datetime import datetime
import bcrypt
from typing import Optional ,List,Dict
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from app.model.roles import Roles
from app.model.suppliers import Supplier
from app.model.miscellaneous import Miscellaneous
from app.services.email_service import EmailService
import secrets
import string ,os

def create_supplier(db: Session, supplier: AddSupplier):
    try:
        db_supplier = Supplier(
            name=supplier.name,
            company=supplier.company,
            email=supplier.email,
            phone=supplier.phone,
            # created_by_id=supplier.created_by_id,
            # created=supplier.created or datetime.utcnow(),
        )

        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)

        return {"message": "Supplier created successfully"}

    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Integrity Error: {str(e.orig)}")

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected Error: {str(e)}")

def get_supplier_by_email(db: Session,email:str)->Optional[Supplier]:
    return db.query(Supplier).filter(Supplier.email==email).first()


def get_all_suppliers(db: Session):
    return db.query(Supplier).all()  # Retrieve all suppliers

def get_supplier_by_id(db: Session, supplier_id: int) -> Optional[AddSupplier]:
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()  # Retrieve supplier by id

def update_supplier(db: Session, supplier_id: int, supplier_data: AddSupplier) -> AddSupplier:
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()

    if not db_supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

    # Check if the email already exists in the database (to avoid unique constraint violation)
    # Update the supplier's details
    db_supplier.name = supplier_data.name or db_supplier.name
    db_supplier.company = supplier_data.company or db_supplier.company
    db_supplier.email = supplier_data.email or db_supplier.email
    db_supplier.phone = supplier_data.phone or db_supplier.phone
   
    try:
        db.commit()
        db.refresh(db_supplier)
        return db_supplier
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Integrity Error: {str(e.orig)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {str(e)}")

def delete_supplier(db: Session, supplier_id: int):
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()

    if not db_supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

    try:
        db.delete(db_supplier)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {str(e)}")

    return {"message": "Supplier deleted successfully"}  # Return a response with a message