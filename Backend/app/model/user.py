from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.roles import Roles
import sys
from app.model.miscellaneous import Miscellaneous


class User(Base):
	__tablename__ = "users"
	user_id = Column(Integer, primary_key=True)
	username = Column(String(length=100), nullable=True)
	email = Column(String(length=60), nullable=True)
	password = Column(String(length=100), nullable=True)
	phone_number = Column(String(length=15), nullable=True)
	role_id= Column(Integer, ForeignKey('roles.role_id', ondelete='CASCADE'))
	status = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
	created_by_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
	created = Column(DateTime, default=datetime.utcnow)
	updated_by_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
	updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
	org_id= Column(Integer, ForeignKey('organizations.org_id', ondelete='CASCADE'))
	
	


