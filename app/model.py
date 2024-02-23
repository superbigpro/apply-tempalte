from pydantic import BaseModel, constr, validator
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean, and_
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

# class User(Base):
#     __tablename__ = "user"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(50), nullable=False, unique=True)
#     password = Column(String(64), nullable=False)
#     school_id = Column(String(30), nullable=False)
#     is_submitted = Column(Boolean, nullable=True, default=False)
#     role = Column(String(10), nullable=False, default="user")

#     applications = relationship('Application', back_populates='user')


# class Application(Base):
#     __tablename__ = "application"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     bio = Column(String(2000), nullable=False)
#     motive = Column(String(2000), nullable=False)
#     plan = Column(String(2000), nullable=False)
#     which_department = Column(String(10), nullable=False)
#     last_modified = Column(DateTime, nullable=True, onupdate=datetime.utcnow())

#     user_id = Column(Integer, ForeignKey('user.id'))
#     user = relationship('User', back_populates='applications')


class Register_example(BaseModel):
    username: str
    school_id : str
    password: str
    re_pw: str

    @validator("school_id")
    def validate_department(cls, param):
        valid_departments = {'C', 'M'}  
        if not param[0].upper() in valid_departments: 
            return False
        return param

class Login_example(BaseModel):
    username: str
    password: str
    
class Application_example(BaseModel):
    bio : str 
    motive : str 
    plan : str 
    which_department : str