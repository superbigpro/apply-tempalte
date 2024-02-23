import os  # Make sure to include this import statement
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, joinedload
from sqlalchemy.sql import extract
from dotenv import load_dotenv

load_dotenv()

MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')

if not MYSQL_PASSWORD:
    raise ValueError("mysql password 환경변수를 찾을 수 없습니다.")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{MYSQL_PASSWORD}@localhost:3306/recruit"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(
    bind=engine
)  

Base = declarative_base()
