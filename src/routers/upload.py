from fastapi import APIRouter, UploadFile, File, HTTPException

from src.core.config import settings
from src.database.models import File as FileModel
from src.utils.telegram import upload_to_telegram
from src.utils.cryptography import encode_base62

router = APIRouter()

@router.post("/")
async def upload_file_route(file: UploadFile = File()):
    content = await file.read()

    if len(content) > settings.MAX_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds the 2 GB limit.")

    file_id = await upload_to_telegram(file, content)
    if file_id:
        file_model = await FileModel.create(
            file_id=file_id,
            file_name=file.filename,
        )

        model_id = await encode_base62(file_model.id)
        return f'{settings.HOST_URL}/{model_id}/{file.filename}'
    else:
        raise HTTPException(status_code=500, detail="Failed to upload file to Telegram or unexpected response.") 