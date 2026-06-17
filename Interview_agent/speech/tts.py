# Text-to-speech module
from gtts import gTTS
import os
import time

def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    file_path = "audio/question.mp3"
    tts.save(file_path)
    
    # Using start to play audio on Windows
    os.system(f"start {file_path}")
    
    # Wait a bit for the audio to play (approximate based on text length)
    # Average reading speed is about 150 words per minute (2.5 words per second)
    words = len(text.split())
    time.sleep(max(3, words / 2.5))
