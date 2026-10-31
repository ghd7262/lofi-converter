import os
from pathlib import Path

STORAGE_DIR = Path(os.environ.get("STORAGE_DIR", "storage"))
ALLOWED_SUFFIXES = (".mp3", ".m4a")
MAX_FILES = int(os.environ.get("MAX_FILES", 10))
MAX_FILE_MB = int(os.environ.get("MAX_FILE_MB", 20))
MAX_SECONDS = int(os.environ.get("MAX_SECONDS", 300))
CLEANUP_AFTER_SECONDS = int(os.environ.get("CLEANUP_AFTER_SECONDS", 300))
