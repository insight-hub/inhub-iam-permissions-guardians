from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, index=True)
    username = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_mail_confirmed = Column(Boolean, default=False)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())
