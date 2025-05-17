import aiohttp
import io

from fastapi.responses import StreamingResponse
from fastapi import UploadFile

from src.core.config import settings

async def upload_to_telegram(file: UploadFile, content: bytes):
    async with aiohttp.ClientSession() as session:
        form_data = aiohttp.FormData()
        form_data.add_field("chat_id", settings.TELEGRAM_CHAT_ID)
        form_data.add_field("document", content, filename=file.filename)

        async with session.post(f"{settings.TELEGRAM_API_URL_BASE}/sendDocument", data=form_data) as response:
            if response.status == 200:
                result = await response.json()
                if "result" in result and "document" in result["result"]:
                    return result["result"]["document"]["file_id"]
                else:
                    return None
            else:
                return None

async def download_from_telegram(file_id: str, filename: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.TELEGRAM_API_URL_BASE}/getFile?file_id={file_id}") as response:
            if response.status == 200:
                file_info = await response.json()
                if "result" in file_info and "file_path" in file_info["result"]:
                    file_path = file_info["result"]["file_path"]
                else:
                    return {"error": "File path not found in Telegram's response."}
            else:
                response_text = await response.text()
                return {"error": f"Failed to fetch file from Telegram. Status code: {response.status}, Response: {response_text}"}

        async with session.get(f"{settings.TELEGRAM_FILE_URL_BASE}/{file_path}") as file_response:
            if file_response.status == 200:
                file_content = await file_response.read()
                return StreamingResponse(
                    io.BytesIO(file_content),
                    media_type="application/octet-stream",
                    headers={"Content-Disposition": f"attachment; filename={filename}"}
                )
            else:
                response_text = await file_response.text()
                return {"error": f"Failed to download file from Telegram. Status code: {file_response.status}, Response: {response_text}"}