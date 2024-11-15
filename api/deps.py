from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from config import Config

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/{Config.API_VERSION}/login")

TokenDep = Annotated[str, Depends(reusable_oauth2)]
