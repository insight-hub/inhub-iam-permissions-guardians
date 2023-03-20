from typing import Literal
from app.models.schemas.rwschema import RWSchema


class UserJoin(RWSchema):
    username: str
    email: str
    password: str


class UserCreated(RWSchema):
    username: str
    email: str


class UserCreatedRes(RWSchema):
    status: int
    user: UserCreated


class UserInResponse(RWSchema):
    pass
