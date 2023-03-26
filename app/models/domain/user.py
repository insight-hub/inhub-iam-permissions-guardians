from app.models.common import DateTimeModelMixin
from app.models.domain.rwmodel import RWModel
from app.services import security


class User(RWModel):
    username: str
    email: str


class UserInDB(DateTimeModelMixin, User):
    hashed_password = ''

    def check_password(self, *, password: str) -> bool:
        return security.varify_password(password, self.hashed_password)

    def change_password(self, *, password: str) -> None:
        self.hashed_password = security.get_password_hash(password)
