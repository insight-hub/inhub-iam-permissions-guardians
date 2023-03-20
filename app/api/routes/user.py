from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.dependenies.database import get_repository
from app.database.errors import EntityDoesNotExist
from app.database.repositories.user import UserRepository
from app.models.schemas.user import UserJoin

router = APIRouter()


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


@router.post('/join')
async def create_user(user: UserJoin = Body(), user_repository: UserRepository = Depends(get_repository(UserRepository))):
    if check_email_taken(user_repository, user.email):
        return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Email already taken")

    if check_username_taken(user_repository, user.username):
        return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Username already taken")

    user = user_repository.create_new_user(user=user)

    return user
