from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.products_service import add_product, get_all_products, get_product_by_id, update_product, delete_product
from app.db.database import get_db
from app.schemas.product_schema import ProductCreate,ProductResponse
from typing import List
from app.model.products import Product

router = APIRouter()

@router.post("/add-product/{supplier_id}", status_code=status.HTTP_201_CREATED, operation_id="create_product_add_product_unique")
def create_product(supplier_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    # Call the service function to add the product
    return add_product(db=db, product=product, supplier_id=supplier_id)

@router.get("/products/", response_model=List[ProductResponse], operation_id="get_all_products_endpoint_unique")
def get_all_products_endpoint(db: Session = Depends(get_db)):
    products = get_all_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

@router.get("/products/{product_id}", response_model=ProductCreate, operation_id="get_product_by_id_endpoint_unique")
def get_product_by_id_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    return product

@router.put("/update_products/{product_id}", response_model=ProductCreate, operation_id="update_product_endpoint_unique")
def update_product_endpoint(product_id: int, product_data: ProductCreate, db: Session = Depends(get_db)):
    updated_product = update_product(db, product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    return updated_product

@router.delete("/products/{product_id}", status_code=status.HTTP_200_OK, operation_id="delete_product_endpoint_unique")
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return delete_product(db, product_id)
