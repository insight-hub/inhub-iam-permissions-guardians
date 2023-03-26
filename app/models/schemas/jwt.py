from datetime import datetime
from enum import EnumType

from pydantic import BaseModel


class JWTSubjects(EnumType):
    access = 'access'
    refresh = 'refresh'


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTUser(BaseModel):
    username: str
