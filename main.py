from fastapi import FastAPI

from config import Config
from routes import api_router

app = FastAPI(title="SCTCE ETLab Backend API", version=Config.VERSION)

app.include_router(api_router, prefix=f"/api/{Config.API_VERSION}")
