from pydantic import BaseModel


class LoginCreds(BaseModel):
    username: str
    password: str
