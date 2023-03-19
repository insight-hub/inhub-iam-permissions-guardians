from fastapi import APIRouter

from app.models.schemas.user import UserInResponse, UserWithToken


router = APIRouter()


@router.post('/join', response_model=UserInResponse)
def create_user():
    return UserInResponse(status=200, user=UserWithToken(username="test", email="test@mail", token="test"))
