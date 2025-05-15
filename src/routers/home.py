from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
async def home():
    try:
        with open('static/help.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return HTTPException(404, "Help file not found")
