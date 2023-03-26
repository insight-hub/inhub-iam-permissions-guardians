from datetime import datetime, timedelta
from typing import Dict

import jwt
from pydantic import ValidationError
from app.models.domain.user import User

from app.models.schemas.jwt import JWTMeta, JWTSubjects, JWTUser

TOKEN_EXPIRED_MINUTES = 60 * 24
ALGORIHTM = "HS256"


def create_access_token(*,
                        jwt_content: Dict[str, str],
                        secret_key: str,
                        expires_delta: timedelta) -> str:
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update(JWTMeta(exp=expire, sub=JWTSubjects.access).dict())
    return jwt.encode(to_encode, secret_key, algorithm=ALGORIHTM)


def create_token_for_user(user: User, secret_key: str) -> str:
    return create_access_token(
        jwt_content=JWTUser(username=user.username).dict(),
        secret_key=secret_key,
        expires_delta=timedelta(minutes=TOKEN_EXPIRED_MINUTES)
    )


def get_user_from_token(token: str, secret_key: str) -> str:
    try:
        return JWTUser(**jwt.decode(token, secret_key, algorithms=[ALGORIHTM])).username
    except jwt.PyJWTError as decode_error:
        raise ValueError('unable to decode jwt token') from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error
