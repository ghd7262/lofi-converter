import numpy as np
import pytest
from fastapi.testclient import TestClient
from pedalboard.io import AudioFile

from app import config, jobs
from app.main import app


def write_tone(path, seconds):
    sr = 44100
    t = np.arange(int(sr * seconds)) / sr
    tone = (0.3 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
    with AudioFile(str(path), "w", sr, 1) as f:
        f.write(tone[np.newaxis, :])
    return path


@pytest.fixture
def tone_mp3(tmp_path):
    return write_tone(tmp_path / "tone.mp3", seconds=2)


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "STORAGE_DIR", tmp_path / "storage")
    jobs.jobs.clear()
    jobs.batches.clear()
    with TestClient(app) as c:
        yield c
