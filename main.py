import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from tortoise.contrib.fastapi import register_tortoise

from src.routers import upload, download, home

from src.core.config import settings
from src.core.logger import InterceptHandler

app = FastAPI()

app.mount("/s", StaticFiles(directory="src/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Make this dynamic
app.include_router(upload.router, prefix="", tags=["upload"])
app.include_router(download.router, prefix="", tags=["download"])
app.include_router(home.router, prefix="", tags=["home"])

register_tortoise(
    app,
    db_url=settings.DB_URI,  # Database URL
    modules={"models": ["src.database.models"]},  # Add your models here
    generate_schemas=True,  # Automatically generate database schema
    add_exception_handlers=True,
)

logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT, log_config=None)
