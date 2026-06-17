import speech_recognition as sr
import pyttsx3
import torch
from transformers import pipeline

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print(f"Calculator: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError:
            speak("Could not request results from Google Speech Recognition service.")
            return ""

print("Loading local AI model (this may take a minute)...")
# Load a small but capable instruct model suitable for logic/math
pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct",
    torch_dtype=torch.float32, # Fallback if GPU is not available
    device_map="auto",
    max_new_tokens=20
)
speak("Model loaded and ready.")

def calculate_with_llm(text):
    if not text:
        return
        
    if "exit" in text or "quit" in text or "stop" in text:
        speak("Goodbye!")
        return False
        
    system_prompt = (
        "You are a mathematical calculator. The user will give you a spoken math problem "
        "(e.g., 'square of 3', 'root 3.5', '5 plus 10'). "
        "You must calculate the result and return ONLY the final numerical answer. "
        "Do not include any words, explanations, or units. Just the number."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]
    
    try:
        result = pipe(messages)
        answer = result[0]['generated_text'][-1]['content'].strip()
        print(f"LLM Answer: {answer}")
        speak(f"The result is {answer}")
    except Exception as e:
        print(f"Error evaluating '{text}': {e}")
        speak("Sorry, I could not evaluate that mathematical expression.")
        
    return True

def main():
    speak("Voice calculator started. What would you like to calculate?")
    running = True
    while running:
        command = listen()
        if command:
            running = calculate_with_llm(command)
        else:
            print("Say 'exit' to stop.")

if __name__ == "__main__":
    main()
