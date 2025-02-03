from pydantic import BaseModel
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.miscellaneous import Miscellaneous
from datetime import datetime
from app.model.organizations import Organizations

class Roles(Base):
    __tablename__ = "roles"
    
    role_id  =Column(Integer, primary_key=True)
    role_name = Column(String(100), nullable=False, unique=True)
    created_by_id = Column(Integer, ForeignKey('users.user_id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, ForeignKey('users.user_id',ondelete= 'CASCADE'))
    updated = Column(DateTime, onupdate=datetime.utcnow)
