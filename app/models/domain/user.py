from pydantic import EmailStr
from app.models.common import DateTimeModelMixin
from app.models.domain.rwmodel import RWModel


class User(RWModel):
    uuid: str
    username: str
    email: EmailStr
    is_mail_confirmed: bool


class UserInDB(DateTimeModelMixin, User):
    hashed_password: str
    pass
