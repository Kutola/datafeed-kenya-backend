from sqlalchemy import Integer, Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func

from ..database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    published_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now() )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True),
        nullable=False, server_default=text('now()')) 
    is_active = Column(Boolean, nullable=False, server_default='TRUE')       