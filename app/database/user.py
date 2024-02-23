from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean, and_
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    school_id = Column(String(30), nullable=False)
    is_submitted = Column(Boolean, nullable=True, default=False)
    role = Column(String(10), nullable=False, default="user")

    applications = relationship('Application', back_populates='user')