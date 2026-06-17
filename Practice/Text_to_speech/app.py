from TTS.api import TTS

# Load model (downloads automatically on first run)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

text = """
Hello, this is a text to speech demo.
The voice is generated locally using an open source model.
"""

tts.tts_to_file(
    text=text,
    file_path="output.wav",
    language="en"
)

print("Audio saved as output.wav")  