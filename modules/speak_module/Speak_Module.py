import subprocess
import sounddevice as sd
import numpy as np

from settings.settings import (
    VOICE_MODEL_PATH,
    SPEAK_BACK
)

class Speak_Module:
    def __init__(self):
        self.MODEL = VOICE_MODEL_PATH

    def speak(self, text):
        try:
            if SPEAK_BACK:
                proc = subprocess.Popen(
                    ["piper", "--model", self.MODEL, "--output_raw"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    bufsize=0
                )
                audio_bytes, _ = proc.communicate(input=text.encode("utf-8"))
                audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
                #Use samplerate to regulate voice pitch
                sd.play(audio_np, samplerate=18000)
                sd.wait()
        except Exception as e:
            print(e)
