from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # TODO: save file to temp/, trigger audio_processor
    return {"filename": file.filename, "status": "received"}
