from fastapi import FastAPI
from routes import api_router
from config import Config

app = FastAPI(title="SCTCE ETLab Backend API", version=Config.VERSION)

app.include_router(api_router, prefix=f"/api/{Config.API_VERSION}")
