
from fastapi import APIRouter

from app.api.routes import authentification, otp

api_router = APIRouter()


api_router.include_router(authentification.router)
api_router.include_router(otp.router, prefix='/otp')
