from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN

from app.api.dependenies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.database.errors import EntityDoesNotExist
from app.database.repositories.user import UserRepository
from app.models.domain.user import UserInDB
from app.services import jwt

# TODO scopes
oauth2_sceme = OAuth2PasswordBearer(tokenUrl='/login')


async def get_current_user(
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        token: str = Depends(oauth2_sceme),
        settings: AppSettings = Depends(get_app_settings)) -> UserInDB:
    try:
        username = jwt.get_user_from_token(
            token, settings.secret_key.get_secret_value())

    except ValueError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                            detail="Wrong credentionals")

    try:
        return user_repo.get_by_username(username=username)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Wrong credentionals"
        )
