from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=True)
    email = Column(String, unique=True, index=True)
    city = Column(String, unique=False, index=True)
    is_active = Column(Boolean, default=True)