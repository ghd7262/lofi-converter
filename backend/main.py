from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, convert

app = FastAPI(title="Lo-fi Converter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(convert.router, prefix="/api")
