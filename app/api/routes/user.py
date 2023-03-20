import json
from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.dependenies.database import get_repository
from app.database.repositories.user import UserRepository
from app.models.schemas.user import UserJoin
from app.services.mail.mail import send_mail
from app.utils.auth import check_email_taken, check_username_taken
from app.utils.otp import get_random_pass
from app.services import redis

router = APIRouter()


@router.post('/join')
async def create_user(user: UserJoin = Body(), user_repository: UserRepository = Depends(get_repository(UserRepository))):
    await send_mail()
