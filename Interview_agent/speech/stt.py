from faster_whisper import WhisperModel

model = WhisperModel(
    "tiny",
    device="cpu"
)

def transcribe(audio_path):

    segments, _ = model.transcribe(audio_path)

    return " ".join(
        segment.text
        for segment in segments
    )