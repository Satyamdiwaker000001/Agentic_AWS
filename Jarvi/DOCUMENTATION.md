# Jarvi (Voice & Gesture OS Assistant) - Documentation

## 1. What does the project do?
This project is a high-tech holographic, computer-vision and voice-controlled virtual assistant named **Jarvi**. It enables hands-free operation of your Windows PC, web browsers, and file management on the `A:` drive. It maps hand landmarks captured via webcam directly to system-wide cursor positions (supporting smooth hover and pinch-to-click operations). Concurrently, a background voice recognition engine parses speech commands to control applications, perform Google searches, trigger browser shortcuts, explore files, and minimize/maximize the camera HUD.

## 2. What is the request flow?
1. **Startup**: The user executes `main.py`.
2. **Initialization**:
   - `HandTracker` checks for OpenCV and MediaPipe and starts the hand tracker state.
   - `GestureEngine` sets up click thresholds and a moving average coordinate smoothing history window.
   - `FileManager` sets up path paths and registers drive search utilities.
   - `HUDRenderer` constructs the diagnostic panel canvas, scanlines, and diagnostic radar.
   - `VoiceEngine` configures the microphone, background SpeechRecognizer, and initialization welcome speech via pyttsx3.
3. **Execution Threads**:
   - **Voice Listening Thread**: Runs asynchronously in the background. It continuously monitors the default microphone, adjusts for ambient noise, translates speech to commands, and handles events:
     - Launches Chrome, Edge, Firefox, Brave, Opera, or default browsers.
     - Performs google queries.
     - Searches and executes files on the `A:` drive recursively.
     - Simulates browser hotkeys (back, refresh, new tab, close tab, scroll page).
     - Launches standard Windows utilities (Notepad, Calculator, Paint).
     - Minimizes, maximizes, or restores the camera HUD window using `pygetwindow`.
   - **Main Camera & Gesture Loop**: Captures web camera frames, performs mirroring, processes joints, maps the index finger tip position to the system monitor screen resolution, and drives `pyautogui` movement and clicks.
     - If the user minimizes the HUD window, the code stops rendering to the screen but keeps the camera capture, hand tracking, and voice engine actively processing background actions.

## 3. Which packages are used and why?
- **`opencv-python` (`cv2`)**: Captures video frames, performs coordinate flips, overlays joint markers, and displays the UI HUD.
- **`mediapipe`**: Detects 21 hand skeletal landmarks.
- **`pyautogui`**: Simulates system-wide cursor movements, clicks, scrolls, and hotkeys.
- **`speechrecognition`**: Captures mic input and performs speech-to-text translation using Google's speech recognition APIs.
- **`pyttsx3`**: Generates text-to-speech feedback lines.
- **`pygetwindow` & `pyrect`**: Controls Windows application window states (checking if minimized, minimizing, restoring).
- **`numpy`**: Performs matrix array manipulation for video frame composition.

## 4. Where does the data come from?
- Video stream: Input from the computer's webcam.
- Voice stream: Spoken words captured via default computer microphone.
- File system: File structures and executable search results recursively fetched from the `A:` drive.

## 5. Where is the data stored?
All joint coordinate traces, speech buffers, and visual outputs are maintained in RAM variables during runtime. No permanent files or logs are stored, and execution targets are invoked directly.

## 6. What is the role of the LLM?
There is no LLM integrated in this local version. Audio instructions are translated to text using standard SpeechRecognition APIs and parsed deterministically for target keyword intents.

## 7. What breaks if the LLM is removed?
Nothing breaks as there are no LLM models or APIs utilized.

## 8. Virtual Environment & Wake Word Protocol
To run the assistant within the dedicated environment, use the local python wrapper:
```bash
.\venv\Scripts\python.exe Jarvi/main.py
```

### Wake Word Protocol
To prevent background conversations from firing false-positive actions, JARVIS operates on a **Wake Word Protocol**:
- **Continuous Monitoring**: The background voice thread captures mic signals.
- **Wake Word Match**: Commands must start with or contain the name **"Jarvis"** or **"Jarvi"** (e.g. *"Jarvis, status"*, *"Jarvis, open Chrome"*).
- **Silent Ignoring**: If the wake word is not detected, the command is discarded.
- **Stark Dialogue**: Incorporates responsive voiced lines mimicking J.A.R.V.I.S., such as *"At your service, sir"*, *"Arc reactor is stable at 100 percent, sir"*, *"Right away, sir"*.
