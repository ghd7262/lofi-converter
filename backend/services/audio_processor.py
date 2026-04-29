import numpy as np
import librosa
import soundfile as sf
from scipy.signal import butter, filtfilt

def apply_lofi(input_path: str, output_path: str) -> str:
    y, sr = librosa.load(input_path, sr=None)

    # 1. Low-pass filter — cut frequencies above 3.5kHz
    b, a = butter(4, 3500 / (sr / 2), btype='low')
    y = filtfilt(b, a, y)

    # 2. Bitcrusher — reduce to 8-bit depth
    y = np.round(y * 32) / 32

    # 3. Vinyl crackle — add subtle noise
    noise = np.random.normal(0, 0.004, len(y))
    y = y + noise

    # 4. Wow & flutter — subtle pitch wobble
    wobble = np.sin(2 * np.pi * 0.5 * np.arange(len(y)) / sr) * 0.002
    y = y * (1 + wobble)

    y = np.clip(y, -1.0, 1.0)
    sf.write(output_path, y, sr)
    return output_path
