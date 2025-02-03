from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


# Supplier model using SQLAlchemy
class Supplier(Base):
    __tablename__ = 'suppliers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(length=30), nullable=False)
    company = Column(String(length=20))
    email = Column(String(length=100), unique=True, nullable=False)  # Added unique=True
    phone = Column(String(length=15))

    products = relationship("Product", back_populates="supplier")

