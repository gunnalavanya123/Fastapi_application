from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class Payments(Base):
    __tablename__ = "payments"
    
    payment_id = Column(Integer, primary_key=True)
    orgId = Column(String(length=50), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    pay_status = Column(String(length=50), nullable=False)
    plan_id = Column(Integer,ForeignKey('plans.plan_id'))

