from typing import Annotated

import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from config import Config
from models import Token

router = APIRouter()
session = requests.Session()


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    payload = {
        "LoginForm[username]": form_data.username,
        "LoginForm[password]": form_data.password,
        "yt0": "",
    }

    headers = {
        "User-Agent": Config.USER_AGENT,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
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

        auth_token = session.cookies.get(Config.COOKIE_KEY)
        return (
            Token(access_token=auth_token)
            if auth_token
            else {
                "status_code": status.HTTP_401_UNAUTHORIZED,
                "message": "Invalid Credentials",
            }
        )
    except Exception as e:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": f"An error occurred: {e}",
        }
