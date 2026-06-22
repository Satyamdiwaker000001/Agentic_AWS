# Virtual Piano (Open Vision Mouse Controller) - Documentation

## 1. What does the project do?
This project is an interactive virtual piano played using hand gestures. It uses the device camera to track hand landmarks and plays different musical notes (C, D, E, F, G, A, B) as sine-wave audio whenever the user's index finger coordinates cross the virtual piano key boundaries on screen.

## 2. What is the request flow?
1. **Startup**: The user runs `main.py` which initializes the camera (`VideoCapture`).
2. **Setup Modules**: `HandTracker` loads MediaPipe solution configs and `InstrumentController` prepares frequency definitions.
3. **Capture & Process Loop**:
   - Camera frames are read, flipped horizontally (mirror view), and resized to 900x600.
   - MediaPipe detects hand landmarks on the processed frames.
   - The script draws 7 white-and-black piano key rectangles at the bottom of the screen (y > 450).
   - If a hand is detected:
     - The index finger tip coordinate (landmark 8) is extracted and highlighted with a red circle.
     - If the index tip y-coordinate is within the piano key boundary (y > 450), the x-coordinate determines which key is selected.
     - If the note changes or a 0.3s cooldown has passed, `piano.play_note` is called.
     - `InstrumentController` generates a sine wave numpy array for 0.25 seconds for the corresponding note frequency and plays it via `sounddevice`.
   - The active note is printed as an overlay on the video feed, and the frame is displayed.
   - Pressing the ESC key terminates the capture loop.

## 3. Which packages are used and why?
- **`opencv-python` (`cv2`)**: Handles camera capturing, visual overlays (rectangles/text), window rendering, and keyboard wait events.
- **`mediapipe`**: Computer vision library used for real-time hands detection and coordinate landmarks extraction.
- **`numpy`**: Generates mathematical coordinates of sine waves for different audio frequencies.
- **`sounddevice`**: Plays generated float32 numpy arrays as sound waves through the system speaker.

## 4. Where does the data come from?
The input data comes from live video frames captured via the user's device camera.

## 5. Where is the data stored?
All evaluations and frames are processed dynamically in RAM. No persistent files or databases are saved.

## 6. What is the role of the LLM?
There is **no LLM model used** in this project. The system relies entirely on standard computer vision regression models and geometry rules.

## 7. What breaks if the LLM is removed?
**Nothing breaks**, since the project has no AI language model dependencies.
