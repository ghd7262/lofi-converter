import asyncio
import shutil
import time

from app import config
from app.jobs import batches, jobs


def cleanup_expired(now=None):
    now = now or time.time()
    for job in list(jobs.values()):
        if job.finished_at and now - job.finished_at >= config.CLEANUP_AFTER_SECONDS:
            shutil.rmtree(job.input_path.parent, ignore_errors=True)
            del jobs[job.job_id]
    for batch in list(batches.values()):
        if not any(job_id in jobs for job_id in batch.job_ids):
            del batches[batch.batch_id]


def reset_storage():
    # Job state is in memory, so files left from a previous run can never be cleaned up or downloaded.
    shutil.rmtree(config.STORAGE_DIR, ignore_errors=True)
    config.STORAGE_DIR.mkdir(parents=True)


async def cleanup_loop(interval_seconds=30):
    while True:
        cleanup_expired()
        await asyncio.sleep(interval_seconds)
