from fastapi import APIRouter, Depends
from app.api.dependenies.authentification import get_current_user

from app.database.orm.user import User


router = APIRouter(tags=["Settings"])


@router.post('/profile')
async def create_new_profile(
        user: User = Depends(get_current_user)
):
    pass
