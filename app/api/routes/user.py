from fastapi import APIRouter, Depends
from app.api.dependenies.database import get_repository

from app.models.schemas.user import UserInResponse
from app.database.repositories.user import UserRepository

router = APIRouter()


@router.post('/join', response_model=UserInResponse)
def create_user(user_repository: UserRepository = Depends(get_repository(UserRepository))):
    pass
