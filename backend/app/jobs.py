import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from app import audio, config


@dataclass
class Job:
    job_id: str
    batch_id: str
    file_name: str
    input_size: int
    input_path: Path
    output_path: Path
    status: str = "queued"
    started_at: float | None = None
    finished_at: float | None = None
    message: str | None = None
    error: dict | None = None


@dataclass
class Batch:
    batch_id: str
    job_ids: list[str]
    created_at: float = field(default_factory=time.time)


# shortcut: in-memory, lost on restart and not shared across processes; upgrade to Redis (Backlog).
batches: dict[str, Batch] = {}
jobs: dict[str, Job] = {}

_convert_lock = threading.Lock()  # one conversion at a time keeps RAM at ~one song


def new_id():
    return uuid.uuid4().hex[:12]


def create_job(batch_id, file_name, input_size, suffix):
    job_id = new_id()
    job_dir = config.STORAGE_DIR / job_id
    job_dir.mkdir(parents=True)
    job = Job(job_id, batch_id, file_name, input_size, job_dir / f"input{suffix}", job_dir / "output.mp3")
    jobs[job_id] = job
    return job


def run_batch(batch_id):
    for job_id in batches[batch_id].job_ids:
        run_job(jobs[job_id])


def run_job(job):
    with _convert_lock:
        job.status = "converting"
        job.started_at = time.time()
        try:
            audio.to_lofi(job.input_path, job.output_path, config.MAX_SECONDS)
            job.status, job.message = "succeeded", "Converted"
        except audio.TooLongError:
            job.status = "failed"
            job.error = {"code": "too_long", "message": f"Max {config.MAX_SECONDS // 60} minutes"}
        except Exception:
            job.status = "failed"
            job.error = {"code": "conversion_error", "message": "Could not convert this file"}
        job.finished_at = time.time()
