import uuid
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


from app.database.db import Base


class User(Base):
    __tablename__ = 'users'

    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    username = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_mail_confirmed = Column(Boolean, default=False)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())
