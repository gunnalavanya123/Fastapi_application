from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class Plan(Base):
    __tablename__ = "plans"

    plan_id = Column(Integer, primary_key=True)
    plan_name = Column(String(length=100), nullable=False)
    price_per_month = Column(Float, nullable=False)