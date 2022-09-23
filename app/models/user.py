from app.config.db import Base

from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer,String

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)