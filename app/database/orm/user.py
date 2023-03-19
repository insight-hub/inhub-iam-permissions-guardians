from sqlalchemy import Column, DateTime, Integer, String

from app.database.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
