import os
import json
import requests
import zipfile
import io
import logging
from vosk import Model, KaldiRecognizer

# --- Configuration Constants ---
#MODEL_NAME = "vosk-model-small-en-us-0.15"
MODEL_NAME = "vosk-model-en-us-0.22-lgraph"
MODEL_PATH = MODEL_NAME
MODEL_DOWNLOAD_URL = f"https://alphacephei.com/vosk/models/{MODEL_NAME}.zip"

# Set up basic logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class VoskRecognizer:
    """
    Real-time speech recognition using Vosk.
    Handles automatic downloading and extraction of the required model.
    """

    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.recognizer = None
        self.is_ready = False

        logging.info(f"Checking for model directory: {MODEL_PATH}...")

        if not self.model_exists():
            logging.warning("Model not found. Initiating automatic download.")
            try:
                self._download_and_extract_model()
            except Exception as e:
                logging.error(f"Failed during model download/extraction: {e}")
                raise RuntimeError("Recognizer initialization failed") from e

        try:
            model = Model(MODEL_PATH)
            self.recognizer = KaldiRecognizer(model, self.sample_rate)
            self.is_ready = True
            logging.info("Vosk Recognizer successfully initialized and ready.")
        except Exception as e:
            logging.error(f"Failed to load Vosk model: {e}")
            raise RuntimeError("Recognizer initialization failed") from e

    def model_exists(self):
        """
        Checks whether the Vosk model directory exists and is non-empty.
        """
        return os.path.isdir(MODEL_PATH) and bool(os.listdir(MODEL_PATH))

    def _download_and_extract_model(self):
        """
        Downloads the Vosk model ZIP and extracts it into the correct folder.
        """
        logging.info(f"Downloading model from: {MODEL_DOWNLOAD_URL}")
        response = requests.get(MODEL_DOWNLOAD_URL, stream=True)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(path=".")
            extracted_dir = zip_file.namelist()[0].split("/")[0]

        if extracted_dir != MODEL_PATH and os.path.exists(extracted_dir):
            os.rename(extracted_dir, MODEL_PATH)

        logging.info(f"Model successfully downloaded and extracted to ./{MODEL_PATH}")

    def listen_once(self, chunk_size=4096):
        """
        Listens for a single utterance via microphone and returns recognized text.
        """
        if not self.is_ready:
            logging.error("Recognizer not ready.")
            return ""

        try:
            import pyaudio
        except ImportError:
            logging.error("PyAudio not installed. Run: pip install pyaudio")
            return ""

        p = pyaudio.PyAudio()
        stream = None
        recognized_text = ""

        try:
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=chunk_size,
            )

            logging.info("--- Listening for one utterance ---")

            while True:
                data = stream.read(chunk_size, exception_on_overflow=False)
                if len(data) == 0:
                    break

                if self.recognizer.AcceptWaveform(data):
                    result_json = json.loads(self.recognizer.Result())
                    recognized_text = result_json.get("text", "")
                    break  # stop after first full result

        except KeyboardInterrupt:
            logging.info("User interrupted listening.")
        except Exception as e:
            logging.error(f"Error during audio streaming: {e}")
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
            p.terminate()

            if not recognized_text:
                try:
                    final_result = json.loads(self.recognizer.FinalResult())
                    recognized_text = final_result.get("text", "")
                except Exception:
                    pass

            logging.info(f"Recognized text: {recognized_text}")
            logging.info("--- Listening stopped ---")

        return recognized_text

    def listen_until_stop(self, chunk_size=4096):
        """
        Continuously listens until the word 'stop' is spoken.
        Returns a single string with all recognized text joined.
        """
        if not self.is_ready:
            logging.error("Recognizer not ready.")
            return ""

        try:
            import pyaudio
        except ImportError:
            logging.error("PyAudio not installed. Run: pip install pyaudio")
            return ""

        p = pyaudio.PyAudio()
        stream = None
        transcript = []

        try:
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=chunk_size,
            )

            logging.info("\n\n--- Listening continuously (say 'stop' to quit) ---\n\n")

            while True:
                data = stream.read(chunk_size, exception_on_overflow=False)
                if len(data) == 0:
                    break

                if self.recognizer.AcceptWaveform(data):
                    result_json = json.loads(self.recognizer.Result())
                    text = result_json.get("text", "")
                    if text:
                        print(f"Recognized: {text}")
                        if "stop" in text.lower():
                            logging.info("Stop command detected, exiting loop.")
                            break
                        transcript.append(text)

        except KeyboardInterrupt:
            logging.info("User interrupted listening.")
        except Exception as e:
            logging.error(f"Error during audio streaming: {e}")
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
            p.terminate()
            logging.info("--- Listening stopped ---")

        final_text = " ".join(transcript).strip()
        logging.info(f"Final transcript: {final_text}")
        return final_text


# --- Example Usage ---
# if __name__ == "__main__":
#     asr = VoskRecognizer()

#     if asr.is_ready:
#         final_text = asr.listen_until_stop()
#         print("\nFinal recognized transcript:")
#         print(final_text)
