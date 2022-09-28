from enum import unique
from app.config.db import Base

from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer,String,TIMESTAMP
from sqlalchemy.sql.expression import text

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
