from fastapi import APIRouter

from api.routes import attendance, info, login

api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(info.router)
api_router.include_router(attendance.router)
