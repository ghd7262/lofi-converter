# lo-fi converter

Upload up to 10 MP3 or M4A files, get lo-fi MP3s back. Private MVP that runs locally in Docker, with a Windows 98–style UI.

The lo-fi effect: slowed to 0.9x like a slowed record (pitch drops too), low-pass filter at 3.5 kHz, and reverb. A 5-minute song converts in about 11 seconds.

## Run

```sh
cp .env.example .env   # first time only; edit to change limits
docker compose up --build
```

Open http://localhost:8080. Stop with `docker compose down`.

## How it works

1. Drop or pick up to 10 files, tick the ones to convert, click **Convert to lo-fi**.
2. The backend accepts valid files and rejects the rest per file (wrong format, over 20 MB, duplicate name).
3. The page polls the batch every second while it's converting. Songs over 5 minutes fail with a message.
4. Click the floppy disk to download. Files are deleted 5 minutes after a job finishes.

| Endpoint | Does |
|---|---|
| `POST /jobs` | Upload 1–10 files as one batch. Returns `batch_id`, accepted jobs, and rejected files with reasons. |
| `GET /batches/{batch_id}` | Status of every job in the batch. |
| `GET /jobs/{job_id}/download` | The converted MP3. |

## Stack

- **Backend:** FastAPI, [Pedalboard](https://github.com/spotify/pedalboard) for audio effects, ffmpeg to decode M4A. Jobs run in the background, one at a time, with state kept in memory (lost on restart).
- **Frontend:** React + Vite, [98.css](https://jdan.github.io/98.css/) for the retro look.
- **Docker:** two containers. nginx serves the frontend on port 8080 and proxies API calls to the backend.

## Settings

Environment variables, set in `.env` (see `.env.example` for defaults): `MAX_FILES`, `MAX_FILE_MB`, `MAX_SECONDS`, `CLEANUP_AFTER_SECONDS`, `STORAGE_DIR`.

## Develop

```sh
# backend (http://localhost:8000)
cd backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
.venv/bin/pytest

# frontend (http://localhost:5173, proxies API calls to the backend)
cd frontend && npm install
npm run dev
npx vitest run
```

The M4A test needs ffmpeg and is skipped without it. Run the full suite inside Docker with `docker compose run --rm --no-deps backend python -m pytest`.

## Project layout

```
backend/app/
  main.py      routes
  jobs.py      in-memory batch/job store, runs conversions
  audio.py     lo-fi transform (Pedalboard)
  cleanup.py   deletes files 5 min after a job finishes
  config.py    settings from env vars
frontend/src/
  components/FileConverter.jsx   the whole UI
  api.js                          backend calls
```

## Roadmap

In progress:
- **Remove vocals** with [Demucs](https://github.com/facebookresearch/demucs). Tested: works, but takes about 10 minutes per song on a laptop CPU in Docker.
- **Target 70–90 BPM** by detecting each song's tempo instead of a fixed 0.9x slowdown.

Later: Redis for job state, a separate worker queue, cloud storage (GCS) with direct uploads, MP4 support, rate limiting.
