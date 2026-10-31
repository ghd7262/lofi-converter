# lo-fi converter

Upload up to 10 MP3s, get lo-fi versions back (low-pass, reverb, slowed 0.9x). Private MVP, runs locally.

## Run

```sh
cp .env.example .env   # first time only; edit to change limits
docker compose up --build
```

Open http://localhost:8080.

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
