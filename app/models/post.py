from app.config.db import Base

from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer,String,Boolean,TIMESTAMP
from sqlalchemy.sql.expression import text

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    published = Column(Boolean, default=True, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 