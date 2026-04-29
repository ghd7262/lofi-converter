from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ConvertURLRequest(BaseModel):
    url: str

@router.post("/convert-url")
async def convert_url(body: ConvertURLRequest):
    # TODO: pass to url_downloader, then audio_processor
    return {"url": body.url, "status": "received"}
