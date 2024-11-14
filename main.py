from fastapi import FastAPI
from routes import api_router
from config import Config

config = Config()
app = FastAPI(title="SCTCE ETLab Backend API", version=config.VERSION)

app.include_router(api_router, prefix=f"/api/{config.API_VERSION}")
