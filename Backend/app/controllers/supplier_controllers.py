from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.model.suppliers import Supplier
from app.schemas.supplier_schema import AddSupplier
from app.services.supplier_service import create_supplier,get_supplier_by_email,get_all_suppliers,get_supplier_by_id,update_supplier,delete_supplier
from app.schemas.organizations_schema import OrganizationUpdate,StatusUpdate
from typing import List,Optional,Dict

router = APIRouter()

@router.post("/add_supplier/", status_code=status.HTTP_201_CREATED)
def create_supplier_endpoint(supplier: AddSupplier, db: Session = Depends(get_db)):
    db_supplier = get_supplier_by_email(db=db, email=supplier.email)
    if db_supplier:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    return create_supplier(db=db, supplier=supplier)  # Fixed argument name

@router.get("/suppliers/", response_model=List[AddSupplier])  # Use AddSupplier schema if you want specific fields in response
def get_all_suppliers_endpoint(db: Session = Depends(get_db)):
    suppliers = get_all_suppliers(db)
    if not suppliers:
        raise HTTPException(status_code=404, detail="No suppliers found")
    return suppliers

@router.get("/suppliers/{supplier_id}", response_model=AddSupplier)
def get_supplier_by_id_endpoint(supplier_id: int, db: Session = Depends(get_db)):
    supplier = get_supplier_by_id(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail=f"Supplier with ID {supplier_id} not found")
    return supplier

@router.put("/suppliers/{supplier_id}", response_model=AddSupplier)
def update_supplier_endpoint(supplier_id: int, supplier_data: AddSupplier, db: Session = Depends(get_db)):
    updated_supplier = update_supplier(db, supplier_id, supplier_data)
    if not updated_supplier:
        raise HTTPException(status_code=404, detail=f"Supplier with ID {supplier_id} not found")
    return updated_supplier

@router.delete("/delete-supplier/{supplier_id}", status_code=status.HTTP_200_OK)
def delete_supplier_endpoint(supplier_id: int, db: Session = Depends(get_db)):
    response = delete_supplier(db=db, supplier_id=supplier_id)
    return response  # Return the response from the service