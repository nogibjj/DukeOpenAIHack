import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play
import os
import queue
import winsound

# Queue to hold audio files
audio_queue = queue.Queue()


def text_to_speech(text, filename):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    with open(filename, "wb") as out:
        out.write(response.audio_content)


class TextFileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_text = ""

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith("commentary.txt"):
            with open("commentary.txt", "r") as f:
                text = f.read()
            new_text = text.replace(self.last_text, "")
            if new_text:
                timestamp = int(time.time())
                audio_file = f"output_{timestamp}.mp3"
                text_to_speech(new_text, audio_file)
                audio_queue.put(audio_file)
                self.last_text = text


def play_audios():
    while True:
        if not audio_queue.empty():
            audio_file = audio_queue.get()
            audio = AudioSegment.from_mp3(audio_file)
            wav_file = "temp.wav"  # Temporary .wav file
            audio.export(wav_file, format="wav")  # Convert to .wav format
            winsound.PlaySound(wav_file, winsound.SND_FILENAME)
            os.remove(audio_file)  # Delete the .mp3 file after playing it
            os.remove(wav_file)  # Delete the .wav file after playing it
        else:
            time.sleep(1)  # Wait for 1 second if the queue is empty


# Create an observer and register the handler
observer = Observer()
observer.schedule(TextFileChangeHandler(), path=".", recursive=False)
observer.start()

# Play audios in the queue
play_audios()

# Stop the observer when done
observer.stop()
observer.join()
