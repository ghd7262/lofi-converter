import asyncio
import shutil
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app import config
from app.cleanup import cleanup_loop, reset_storage
from app.jobs import Batch, batches, create_job, jobs, new_id, run_batch


@asynccontextmanager
async def lifespan(app):
    reset_storage()
    task = asyncio.create_task(cleanup_loop())
    yield
    task.cancel()


app = FastAPI(title="Lo-fi Converter API", lifespan=lifespan)


def rejection(file_name, code, message):
    return {"file_name": file_name, "error": {"code": code, "message": message}}


@app.post("/jobs", status_code=202)
def create_jobs(background_tasks: BackgroundTasks, files: list[UploadFile] = []):  # default so zero files gets our 400, not 422
    if not 1 <= len(files) <= config.MAX_FILES:
        raise HTTPException(400, f"Upload 1 to {config.MAX_FILES} files")

    batch_id = new_id()
    accepted, rejected, seen = [], [], set()
    for upload in files:
        name = upload.filename or ""
        if name in seen:
            rejected.append(rejection(name, "duplicate_name", "Same file name already in this batch"))
        elif not name.lower().endswith(".mp3"):
            rejected.append(rejection(name, "unsupported_format", "MP3 files only"))
        elif upload.size > config.MAX_FILE_MB * 1024 * 1024:
            rejected.append(rejection(name, "too_large", f"Max {config.MAX_FILE_MB} MB"))
        else:
            job = create_job(batch_id, name, upload.size)
            with open(job.input_path, "wb") as out:
                shutil.copyfileobj(upload.file, out)
            accepted.append(job)
        seen.add(name)

    batches[batch_id] = Batch(batch_id, [job.job_id for job in accepted])
    background_tasks.add_task(run_batch, batch_id)
    return {
        "batch_id": batch_id,
        "jobs": [{"job_id": job.job_id, "file_name": job.file_name} for job in accepted],
        "rejected": rejected,
    }


@app.get("/batches/{batch_id}")
def get_batch(batch_id: str):
    batch = batches.get(batch_id)
    if not batch:
        raise HTTPException(404, "Unknown batch")
    return {
        "batch_id": batch_id,
        "jobs": [
            {
                "job_id": job.job_id,
                "file_name": job.file_name,
                "status": job.status,
                "message": job.message,
                "error": job.error,
            }
            for job in (jobs[job_id] for job_id in batch.job_ids if job_id in jobs)
        ],
    }


@app.get("/jobs/{job_id}/download")
def download(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Unknown job, or its file was cleaned up")
    if job.status != "succeeded":
        raise HTTPException(409, "Job has not finished converting")
    return FileResponse(job.output_path, media_type="audio/mpeg", filename=f"{Path(job.file_name).stem}-lofi.mp3")
