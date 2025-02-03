# services/product_service.py
from sqlalchemy.orm import Session
from app.model.products import Product
from app.model.suppliers import Supplier
from app.schemas.product_schema import ProductCreate
from fastapi import HTTPException, status
from typing import List,Optional
from sqlalchemy.exc import IntegrityError,SQLAlchemyError

def add_product(db: Session, product: ProductCreate, supplier_id: int):
    # Check if the supplier exists
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

    # Create the product entry
    db_product = Product(
        name=product.name,
        quantityinstock=product.quantityinstock,
        quantity_sold=product.quantity_sold,
        unit_price=product.unit_price,
        revenue=product.revenue,
        supplied_by=supplier_id  # Associate the product with the supplier
    )

    # Add and commit the product to the database
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

def get_all_products(db: Session):
    # Fetch all products from the database
    products = db.query(Product).all()
    return products

def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.product_id == product_id).first()

def update_product(db: Session, product_id: int, product_data: ProductCreate) -> Optional[Product]:
    db_product = db.query(Product).filter(Product.product_id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Update the product's details
    db_product.name = product_data.name or db_product.name
    db_product.quantityinstock = product_data.quantityinstock or db_product.quantityinstock
    db_product.quantity_sold = product_data.quantity_sold or db_product.quantity_sold
    db_product.unit_price = product_data.unit_price or db_product.unit_price
    db_product.revenue = product_data.revenue or db_product.revenue

    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {str(e)}")

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    try:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {str(e)}")
