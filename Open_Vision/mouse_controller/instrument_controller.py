import numpy as np
import sounddevice as sd


class InstrumentController:

    def __init__(self):

        self.sample_rate = 44100

        self.notes = {
            "C": 261.63,
            "D": 293.66,
            "E": 329.63,
            "F": 349.23,
            "G": 392.00,
            "A": 440.00,
            "B": 493.88
        }

    def play_note(self, note):

        frequency = self.notes[note]

        duration = 0.25

        t = np.linspace(
            0,
            duration,
            int(self.sample_rate * duration),
            False
        )

        wave = np.sin(
            2 * np.pi * frequency * t
        )

        audio = wave.astype(np.float32)

        sd.play(audio, self.sample_rate)