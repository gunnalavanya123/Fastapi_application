from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
class Miscellaneous(Base):
    __tablename__ = "miscellaneous"
    miscellaneous_id = Column(Integer,primary_key=True)
    type = Column(String(length=100), nullable=True)
    value = Column(String(length=100),nullable=True)
    created_by_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, ForeignKey('users.user_id',ondelete= 'CASCADE'))
    updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)       
    created_by = relationship('User', foreign_keys=[created_by_id])    
    