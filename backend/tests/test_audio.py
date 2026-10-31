import pytest
from pedalboard.io import AudioFile

from app.audio import TooLongError, to_lofi


def test_to_lofi_slows_down_and_writes_mp3(tone_mp3, tmp_path):
    out = tmp_path / "out.mp3"
    to_lofi(tone_mp3, out, max_seconds=300)
    with AudioFile(str(out)) as f:
        assert f.samplerate == 44100
        assert f.duration == pytest.approx(2 / 0.9, abs=0.1)


def test_to_lofi_rejects_too_long(tone_mp3, tmp_path):
    with pytest.raises(TooLongError):
        to_lofi(tone_mp3, tmp_path / "out.mp3", max_seconds=1)
