import subprocess

from pedalboard import Pedalboard, LowpassFilter, Reverb
from pedalboard.io import AudioFile

OUTPUT_SAMPLE_RATE = 44100  # MP3 only supports 32k / 44.1k / 48k
SLOWDOWN = 0.9

BOARD = Pedalboard([
    LowpassFilter(cutoff_frequency_hz=3500),
    Reverb(room_size=0.5, wet_level=0.25),
])


class TooLongError(Exception):
    pass


def decode_to_wav(path):
    # Pedalboard can't read M4A/AAC on Linux, so ffmpeg decodes it first.
    wav = path.with_suffix(".wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(path), "-vn", str(wav)], check=True, timeout=60)
    return wav


def to_lofi(input_path, output_path, max_seconds):
    if input_path.suffix == ".m4a":
        input_path = decode_to_wav(input_path)
    with AudioFile(str(input_path)) as f:  # Pedalboard rejects Path objects
        if round(f.duration) > max_seconds:  # MP3 padding makes a 5:00 track read as ~300.03s
            raise TooLongError(f"{f.duration:.0f}s > {max_seconds}s")
        # Read at a higher rate, write at the normal rate: plays back slower and lower, like a slowed record.
        with f.resampled_to(OUTPUT_SAMPLE_RATE / SLOWDOWN) as r:
            audio = r.read(r.frames)
    out = BOARD(audio, OUTPUT_SAMPLE_RATE)
    with AudioFile(str(output_path), "w", OUTPUT_SAMPLE_RATE, out.shape[0]) as f:
        f.write(out)
