import os
import json
import requests
import zipfile
import io
import logging
from vosk import Model, KaldiRecognizer

# --- Configuration Constants ---
MODEL_NAME = "vosk-model-small-en-us-0.15"
#MODEL_NAME = "vosk-model-en-us-0.22-lgraph"
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

    def listen_once(self, chunk_size=1024):
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
                try:
                    data = stream.read(chunk_size, exception_on_overflow=False)
                    if len(data) == 0:
                        break

                    if self.recognizer.AcceptWaveform(data):
                        result_json = json.loads(self.recognizer.Result())
                        recognized_text = result_json.get("text", "")
                        break  # stop after first full result
                except Exception as e:
                    logging.error(f"Error during audio streaming: {e}")
                    break
                except KeyboardInterrupt:
                    logging.info("User interrupted listening.")
                    break

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

    def listen_until_stop(self, chunk_size=1024):
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
                try:
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
                except Exception as e:
                    logging.error(f"Error during audio streaming: {e}")
                    break
                except KeyboardInterrupt:
                    logging.info("User interrupted listening.")
                    break    

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

    def continuous_listening(self, chunk_size=1024):
        """
        Continuously listens until silence is detected or max duration exceeded.
        Returns a single string with all recognized text joined.
        """
        if not self.is_ready:
            logging.error("Recognizer not ready.")
            return ""

        try:
            import pyaudio, numpy as np, json, time
        except ImportError:
            logging.error("Required modules missing. Run: pip install pyaudio numpy")
            return ""

        p = pyaudio.PyAudio()
        stream = None
        transcript = []

        # Silence detection parameters
        silence_threshold = 50      # adjust per environment
        silence_duration = 10.0      # seconds of quiet before stop
        max_duration = 20.0         # safety limit in seconds
        silence_start = None
        speech_detected = False
        start_time = time.time()

        try:
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=chunk_size,
            )

            logging.info("\n\n--- Listening continuously (auto-stops on silence) ---\n\n")

            while True:
                # Stop if max duration reached
                if time.time() - start_time > max_duration:
                    logging.info("Max listening time reached, stopping.")
                    break

                try:
                    data = stream.read(chunk_size, exception_on_overflow=False)
                    if len(data) == 0:
                        continue

                    # Compute RMS safely
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    if audio_data.size == 0:
                        continue

                    float_data = audio_data.astype(np.float64)
                    float_data = np.clip(float_data, -32768, 32767)

                    mean_square = np.mean(np.square(float_data)) if float_data.size else 0.0
                    rms = float(np.sqrt(mean_square)) if mean_square > 0 else 0.0

                    # Debug: monitor RMS levels (comment out after tuning)
                    # print(f"RMS: {rms:.2f}")

                    # Silence check
                    if rms < silence_threshold:
                        if silence_start is None:
                            silence_start = time.time()
                        elif time.time() - silence_start > silence_duration:
                            logging.info("Silence threshold reached, stopping listening.")
                            break
                    else:
                        silence_start = None

                    # Recognition
                    if self.recognizer.AcceptWaveform(data):
                        result_json = json.loads(self.recognizer.Result())
                        text = result_json.get("text", "")
                        if text:
                            print(f"Recognized: {text}")
                            transcript.append(text)
                            speech_detected = True

                except KeyboardInterrupt:
                    logging.info("User interrupted listening.")
                    break
                except Exception as e:
                    logging.error(f"Error during audio streaming: {e}")
                    break

        except Exception as e:
            logging.error(f"Error initializing audio stream: {e}")
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
            p.terminate()
            logging.info("--- Listening stopped ---")

        final_text = " ".join(transcript).strip()

        # Fallback when nothing said
        if not speech_detected or not final_text:
            final_text = "User said nothing."

        logging.info(f"Final transcript: {final_text}")
        return final_text



