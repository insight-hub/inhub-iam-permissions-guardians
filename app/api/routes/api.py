
from fastapi import APIRouter

from app.api.routes import user

api_router = APIRouter()


@api_router.get('/ping')
async def pong():
    return {'status': 200, 'message': 'pong'}

api_router.include_router(user.router, prefix='/user')
