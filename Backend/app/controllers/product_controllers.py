# controllers/product_controllers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from app.services.products_service import add_product,get_all_products,get_product_by_id,update_product,delete_product
from app.db.database import get_db
from app.schemas.product_schema import ProductCreate
from typing import List,Optional,Dict
from app.model.products import Product

router = APIRouter()

@router.post("/add-product/{supplier_id}", status_code=status.HTTP_201_CREATED)
def create_product(supplier_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    # Call the service function to add the product
    return add_product(db=db, product=product, supplier_id=supplier_id)

@router.get("/products/", response_model=List[ProductCreate])  # Use AddSupplier schema if you want specific fields in response
def get_all_products_endpoint(db: Session = Depends(get_db)):
    roducts = get_all_products(db)
    if not roducts:
        raise HTTPException(status_code=404, detail="No suppliers found")
    return roducts

@router.get("/products/{product_id}", response_model=ProductCreate)
def get_product_by_id_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    return product

@router.put("/products/{product_id}", response_model=ProductCreate)
def update_product_endpoint(product_id: int, product_data: ProductCreate, db: Session = Depends(get_db)):
    updated_product = update_product(db, product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    return updated_product

@router.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return delete_product(db, product_id)

