import uuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.sql import func

from app.database.db import Base


class Profile(Base):
    __tablename__ = 'profiles'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(30), default="username")
    company_name = Column(String(30))
    bio = Column(String)
    location = Column(String(30))
    # TODO ForeignKey Languages table
    prefere_language = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())

    username = mapped_column(String, ForeignKey('users.username'))
    user = relationship('User', back_populates='profile')
