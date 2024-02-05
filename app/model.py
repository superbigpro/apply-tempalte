from pydantic import BaseModel, constr, validator
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean, and_
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    school_id = Column(String(30), nullable=False)
    is_submitted = Column(Boolean, nullable=False, default=False)
    role = Column(String(10), nullable=False, default="user")

    applications = relationship('Application', back_populates='user')


class Application(Base):
    __tablename__ = "application"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    phone = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='applications')


class Register_example(BaseModel):
    username: constr(min_length=6, max_length=30)
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
    email : str 
    content : str 
    phone : str 
    