from fastapi import APIRouter, status
from config import Config
from models import LoginCreds
from bs4 import BeautifulSoup
import requests

router = APIRouter()
session = requests.Session()


@router.post("/login")
async def login(creds: LoginCreds):
    payload = {
        "LoginForm[username]": creds.username,
        "LoginForm[password]": creds.password,
        "yt0": "",
    }

    headers = {
        "User-Agent": Config.USER_AGENT,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = session.post(
        f"{Config.BASE_URL}/user/login", data=payload, headers=headers
    )

    parsed_response = BeautifulSoup(response.text, "html.parser")
    title = parsed_response.title.text.lower()  # type: ignore
    if "login" in title:
        return {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "message": "Invalid Credentials",
        }

    auth_token = session.cookies.get_dict()[Config.COOKIE_KEY]
    return {"status_code": status.HTTP_200_OK, "auth_token": auth_token}
