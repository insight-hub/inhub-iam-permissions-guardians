from app.database.repositories.user import UserRepository
from app.database.errors import EntityDoesNotExist


def check_username_taken(repo: UserRepository, username: str):
    try:
        repo.get_by_username(username=username)
    except EntityDoesNotExist:
        return False

    return True


def check_email_taken(repo: UserRepository, email: str):
    try:
        repo.get_by_email(email=email)
    except EntityDoesNotExist:
        return False

    return True
