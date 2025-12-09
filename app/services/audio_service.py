from openai import OpenAI
from io import BytesIO

client = OpenAI()

def transcribe_audio(audio_bytes: bytes):
    """
    Use OpenAI Whisper to transcribe audio files.
    """
    audio_stream = BytesIO(audio_bytes)
    audio_stream.name = "audio.wav"

    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_stream
    )

    return transcript["text"]
