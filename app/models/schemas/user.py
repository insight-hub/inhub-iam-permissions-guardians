from app.models.schemas.rwschema import RWSchema


class UserJoin(RWSchema):
    username: str
    email: str
    password: str
