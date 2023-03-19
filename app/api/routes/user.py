from fastapi import APIRouter, Depends
from app.api.dependenies.database import get_repository

from app.database.repositories.user import UserRepository

router = APIRouter()


@router.post('/join')
async def create_user(user_repository: UserRepository = Depends(get_repository(UserRepository))):
    pass
