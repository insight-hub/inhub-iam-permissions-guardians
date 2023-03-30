from fastapi import APIRouter


router = APIRouter()


@router.get('/{username}')
async def read_profile():
    pass
