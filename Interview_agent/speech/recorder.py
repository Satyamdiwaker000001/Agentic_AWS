import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(
    filename,
    duration=20,
    sample_rate=16000
):

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1
    )

    sd.wait()

    write(
        filename,
        sample_rate,
        audio
    )