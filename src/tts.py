from google.cloud import texttospeech


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


with open("commentary.txt", "r") as f:
    text = f.read()
print(text)

text_to_speech(text, "output.mp3")
