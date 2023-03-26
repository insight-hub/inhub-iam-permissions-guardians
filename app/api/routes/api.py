
from fastapi import APIRouter

from app.api.routes import authentification, user

api_router = APIRouter()


api_router.include_router(user.router, prefix='/user')
api_router.include_router(authentification.router)
