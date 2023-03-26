from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from app.models.domain.user import User
from app.models.schemas.rwschema import RWSchema


class UserJoin(RWSchema):
    username: str
    email: str
    password: str


class UserCreated(RWSchema):
    id: UUID
    username: str
    email: str


class UserCreatedRes(RWSchema):
    status: int
    user: UserCreated


class UserInUpdate(RWSchema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_mail_confirmed: Optional[bool] = None


class UserWithToken(User, RWSchema):
    token: str


class UserInResponse(RWSchema):
    status: int
    user: UserWithToken
