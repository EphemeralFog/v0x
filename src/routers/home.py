from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from src.core.config import settings

router = APIRouter()

@router.get("/")
async def home():
    try:
        with open('src/static/help.txt', 'r') as file:
            content = file.read()
            return PlainTextResponse(content=content.replace("\\n", "\n").format(settings.HOST_URL))
    except FileNotFoundError:
        return HTTPException(404, "Help file not found")
