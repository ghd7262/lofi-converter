import numpy as np
import soundfile as sf
import tempfile
import os
from services.audio_processor import apply_lofi

def test_lofi_output_is_created():
    sr = 22050
    y = np.zeros(sr)  # 1 second of silence

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as inp:
        sf.write(inp.name, y, sr)
        input_path = inp.name

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as out:
        output_path = out.name

    try:
        result = apply_lofi(input_path, output_path)
        assert os.path.exists(result)
    finally:
        os.unlink(input_path)
        os.unlink(output_path)
