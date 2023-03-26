from passlib.context import CryptContext

CLIENT_SECRET = "SECRET"
ALGORITM = "HS256"
TOKEN_EXPIRED_MINUTES = 1

pwd_context = CryptContext(schemes=['bycript'], deprecated='auto')


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def varify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
