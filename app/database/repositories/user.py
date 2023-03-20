from app.database.errors import EntityDoesNotExist
from app.database.repositories.base import BaseRespository
from app.database.orm.user import User
from app.models.schemas.user import UserJoin


class UserRepository(BaseRespository):
    def get_by_email(self, *, email: str):
        user_row = self.connection.query(
            User).filter(User.email == email).first()

        if user_row:
            return user_row

        raise EntityDoesNotExist

    def get_by_username(self, *, username: str):
        user_row = self.connection.query(
            User).filter(User.username == username).first()

        if user_row:
            return user_row

        raise EntityDoesNotExist

    def create_new_user(self, *, user: UserJoin):
        db_user = User(username=user.username,
                       email=user.email, hashed_password="test")

        self.connection.add(db_user)
        self.connection.commit()
        self.connection.refresh(db_user)

        return db_user
