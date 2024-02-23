from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean, and_
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Application(Base):
    __tablename__ = "application"
    id = Column(Integer, primary_key=True, autoincrement=True)
    bio = Column(String(2000), nullable=False)
    motive = Column(String(2000), nullable=False)
    plan = Column(String(2000), nullable=False)
    which_department = Column(String(10), nullable=False)
    last_modified = Column(DateTime, nullable=True, onupdate=datetime.utcnow())

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='applications')