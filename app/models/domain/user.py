from app.models.common import DateTimeModelMixin
from app.models.domain.rwmodel import RWModel


class User(RWModel):
    username: str
    email: str


class UserInDB(DateTimeModelMixin, User):
    pass
