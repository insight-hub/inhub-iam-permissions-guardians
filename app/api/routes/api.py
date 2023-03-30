
from fastapi import APIRouter

from app.api.routes import (
    authentification,
    otp,
    settings,
    profile
)

api_router = APIRouter()


api_router.include_router(authentification.router)
api_router.include_router(otp.router, prefix='/otp')
api_router.include_router(settings.router, prefix='/settings')
api_router.include_router(profile.router)
