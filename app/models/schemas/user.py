from app.models.domain.user import User
from app.models.schemas.rwschema import RWSchema


class UserJoin(RWSchema):
    username: str
    email: str
    password: str


class UserWithToken(User):
    token: str


class UserInResponse(RWSchema):
    user: UserWithToken
