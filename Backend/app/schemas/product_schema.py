# schemas/product_schema.py
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    quantityinstock: Optional[int] = 0
    quantity_sold: Optional[int] = 0
    unit_price: Decimal = 0.00
    revenue: Decimal = 0.00

class ProductResponse(BaseModel):
    product_id: int  # Add this field to include the ID in response
    name: str
    quantityinstock: Optional[int] = 0
    quantity_sold: Optional[int] = 0
    unit_price: Decimal = 0.00
    revenue: Decimal = 0.00


    class Config:
        orm_mode = True
