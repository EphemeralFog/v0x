from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/")
async def home():
    try:
        with open('src/static/help.txt', 'r') as file:
            content = file.read()
            return PlainTextResponse(content=content.replace("\\n", "\n"))
    except FileNotFoundError:
        return HTTPException(404, "Help file not found")
