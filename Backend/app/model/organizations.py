from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class Organizations(Base):
    __tablename__ = "organizations"
    
    org_id = Column(Integer, primary_key=True)
    organization_iD =Column(String(length=100), nullable=True)
    org_name = Column(String(length=100), nullable=True)
    email = Column(String(length=60), nullable=True) 
    status = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id'))
    created_by_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True) 
    email_sent = Column(Boolean, default=False)    
