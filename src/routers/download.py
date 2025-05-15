from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from src.utils.telegram import download_from_telegram
from src.utils.cryptography import decode_base62
from src.database.models import File

router = APIRouter()

@router.get("/{entry_id}/{filename}")
async def download_file_route(entry_id: str, filename: str):
    entry_id = await decode_base62(entry_id)
    entry = await File.get_or_none(id=entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="File not found in the database.")
    if entry.file_name != filename:
        raise HTTPException(status_code=400, detail="Filename mismatch.")
    response = await download_from_telegram(entry.file_id, filename)
    if isinstance(response, StreamingResponse):
        return response
    elif isinstance(response, dict) and "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    else:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while trying to download the file.") 