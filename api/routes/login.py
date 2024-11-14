from fastapi import APIRouter
from models import LoginCreds

router = APIRouter()


@router.post("/login")
async def login(creds: LoginCreds):
    return {"message": "Hellow, World!"}
