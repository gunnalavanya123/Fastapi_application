# models/product.py
from typing import Sequence
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.types import DECIMAL
from app.db.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=100), nullable=False)
    quantityinstock = Column(Integer, default=0)
    quantity_sold = Column(Integer, default=0)
    unit_price = Column(DECIMAL(8, 2), default=0.00)
    revenue = Column(DECIMAL(20, 2), default=0.00)
    
    # Ensure the foreign key is correctly defined to reference the suppliers table's id column
    supplied_by = Column(Integer, ForeignKey('suppliers.id'))  # Correctly referencing 'suppliers.id'
    
    supplier = relationship("Supplier", back_populates="products")  # Relationship for easy access
