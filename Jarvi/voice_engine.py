import threading
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess
import pyautogui

class VoiceEngine(threading.Thread):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app  # Reference to the main application
        self.daemon = True
        self.running = True
        
        # Initialize text-to-speech
        try:
            self.tts = pyttsx3.init()
            voices = self.tts.getProperty('voices')
            if voices:
                # Default to the first available voice
                self.tts.setProperty('voice', voices[0].id)
            self.tts.setProperty('rate', 175)  # Dynamic, clean Jarvis speech rate
        except Exception as e:
            print(f"[Voice Engine] TTS Init Warning: {e}")
            self.tts = None

        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        
    def speak(self, text):
        print(f"[JARVIS]: {text}", flush=True)
        if self.tts:
            try:
                self.tts.say(text)
                self.tts.runAndWait()
            except Exception as e:
                print(f"[Voice Engine] Speech error: {e}", flush=True)

    def run(self):
        # Perform ambient noise calibration ONCE at startup
        try:
            with sr.Microphone() as source:
                print("[Voice Engine] Calibrating microphone for ambient noise...", flush=True)
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                print(f"[Voice Engine] Calibration complete. Initial energy threshold: {self.recognizer.energy_threshold:.2f}", flush=True)
        except Exception as e:
            print(f"[Voice Engine] Initial calibration error: {e}", flush=True)

        self.speak("Voice systems initialized and online, sir.")
        
        while self.running:
            try:
                with sr.Microphone() as source:
                    print("[Voice Engine] Listening...", flush=True)
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                
                try:
                    raw_command = self.recognizer.recognize_google(audio).lower().strip()
                    print(f"[Voice Engine] Heard: '{raw_command}'", flush=True)
                    
                    # Wake word check: "Jarvis" or "Jarvi" must be present to activate
                    if "jarvis" in raw_command or "jarvi" in raw_command:
                        # Extract the clean command without the wake word
                        clean_command = raw_command.replace("jarvis", "").replace("jarvi", "").strip()
                        
                        if not clean_command:
                            self.speak("At your service, sir. What are your instructions?")
                        else:
                            self.process_command(clean_command)
                    else:
                        print("[Voice Engine] Wake word ('Jarvis'/'Jarvi') not detected. Ignoring command.", flush=True)
                        
                except sr.UnknownValueError:
                    pass  # Ignore background chatter/noise
                except sr.RequestError as e:

                    print(f"[Voice Engine] Speech Recognition API request error: {e}")
            except Exception as e:
                print(f"[Voice Engine] Microphone or audio subsystem error: {e}")
                # Wait before retrying to prevent CPU spinning if microphone is blocked/busy
                threading.Event().wait(3.0)

                
    def process_command(self, command):
        print(f"[Voice Engine] Processing: '{command}'")
        
        # 1. System Shutdown commands
        if any(w in command for w in ["stop", "shutdown", "exit", "deactivate", "power down"]):
            self.speak("Very well, sir. Deactivating all protocols and powering down. Goodbye.")
            self.main_app.stop()
            self.running = False
            return
            
        # 2. General Greetings
        if any(w in command for w in ["hello", "hi", "hey", "are you there"]):
            self.speak("Hello, sir. Ready for your instructions.")
            return

        # 3. Stark Diagnostics & Dialogues
        if any(w in command for w in ["help", "instructions", "manual", "how to operate"]):
            self.speak("I can be operated using natural hand gestures and voice instructions, sir. "
                       "Use your right hand to move the system cursor. Pinch your index finger and thumb together to click. "
                       "Make a fist with your left hand to go back. "
                       "For voice instructions, address me with my name followed by your command, such as: "
                       "'Jarvis, open Chrome', 'Jarvis, search for Stark Industries', or 'Jarvis, run diagnostics'.")
            return
        elif "status" in command or "diagnostics" in command:
            self.speak("All systems are functioning within normal parameters, sir. Core reactor is stable. Hand tracking camera and voice networks are online.")
            return
        elif "reactor" in command or "power level" in command or "core status" in command:
            self.speak("Arc reactor core is operating at peak capacity, sir. Core energy levels are stable at 100 percent.")
            return
        elif any(w in command for w in ["who are you", "what are you", "introduce yourself"]):
            self.speak("I am JARVIS, your virtual personal assistant. I manage your PC cursor tracking, A drive search networks, and execute software on your commands.")
            return
        elif "thank you" in command or "thanks" in command:
            self.speak("You are most welcome, sir. Happy to assist.")
            return


        # 4. Window State Control (Minimizing/Maximizing camera window)
        if "minimize" in command:
            self.speak("Minimizing main diagnostics window, sir.")
            self.main_app.minimize_window()
            return
        elif any(w in command for w in ["maximize", "restore", "open camera", "show window"]):
            self.speak("Restoring diagnostics window, sir.")
            self.main_app.restore_window()
            return

        # 5. Web Browsers launch commands
        browsers = {
            "chrome": ["chrome", "google-chrome"],
            "edge": ["msedge"],
            "firefox": ["firefox"],
            "brave": ["brave"],
            "opera": ["opera"]
        }
        
        opened_browser = False
        for name, cmds in browsers.items():
            if f"open {name}" in command or f"launch {name}" in command:
                self.speak(f"Right away, sir. Launching {name.capitalize()}.")
                try:
                    subprocess.Popen(f"start {cmds[0]}", shell=True)
                    opened_browser = True
                except Exception as e:
                    print(f"Error launching browser {name} via terminal: {e}")
                    webbrowser.open("http://www.google.com")
                    opened_browser = True
                break
                
        if not opened_browser and "open browser" in command:
            self.speak("Opening default web browser, sir.")
            webbrowser.open("http://www.google.com")
            opened_browser = True
            
        if opened_browser:
            return

        # 6. Google Search engine queries
        if "search for" in command or "google" in command:
            query = ""
            if "search for" in command:
                query = command.split("search for")[-1].strip()
            elif "google" in command:
                query = command.split("google")[-1].strip()
            
            if query:
                self.speak(f"Searching database and Google for '{query}', sir.")
                url = f"https://www.google.com/search?q={query}"
                webbrowser.open(url)
                return

        # 7. Recursive File Search and execution in A: drive
        if "search drive a for" in command or "search a drive for" in command or "find file" in command:
            filename = ""
            if "search drive a for" in command:
                filename = command.split("search drive a for")[-1].strip()
            elif "search a drive for" in command:
                filename = command.split("search a drive for")[-1].strip()
            elif "find file" in command:
                filename = command.split("find file")[-1].strip()
                
            if filename:
                self.speak(f"Searching A drive storage blocks for '{filename}', sir.")
                self.main_app.search_and_run_file(filename)
                return
                
        # 8. Executing files/applications by name
        if "run file" in command or "execute" in command or "open file" in command:
            filename = ""
            if "run file" in command:
                filename = command.split("run file")[-1].strip()
            elif "execute" in command:
                filename = command.split("execute")[-1].strip()
            elif "open file" in command:
                filename = command.split("open file")[-1].strip()
                
            if filename:
                self.speak(f"Right away, sir. Locating and executing '{filename}'.")
                self.main_app.search_and_run_file(filename)
                return

        # 9. Launch Native Windows apps
        native_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "explorer": "explorer.exe",
            "task manager": "taskmgr.exe"
        }
        for app_name, app_exe in native_apps.items():
            if f"run {app_name}" in command or f"open {app_name}" in command:
                self.speak(f"Right away, sir. Launching {app_name.capitalize()}.")
                try:
                    subprocess.Popen(app_exe, shell=True)
                except Exception as e:
                    print(f"Error launching native application {app_name}: {e}")
                return

        # 10. General system-wide controls (simulated keys)
        if "go back" in command:
            self.speak("Navigating backward.")
            pyautogui.hotkey('alt', 'left')
            return
        elif "refresh" in command:
            self.speak("Refreshing window.")
            pyautogui.press('f5')
            return
        elif "new tab" in command:
            self.speak("Opening new tab.")
            pyautogui.hotkey('ctrl', 't')
            return
        elif "close tab" in command:
            self.speak("Closing active tab.")
            pyautogui.hotkey('ctrl', 'w')
            return
        elif "scroll down" in command:
            self.speak("Scrolling page down, sir.")
            pyautogui.scroll(-500)
            return
        elif "scroll up" in command:
            self.speak("Scrolling page up, sir.")
            pyautogui.scroll(500)
            return
        
        # Fallback for unrecognized instruction containing wake word
        self.speak("Sorry sir, I heard you say " + command + ", but that is not in my database protocols.")
