# Spider-Man Web Throw (Open Vision Web Throw) - Documentation

## 1. What does the project do?
This project is an interactive screen overlay animation triggered by hand gestures. It uses the camera feed to detect if the user makes a Spider-Man web-shooting gesture. If active, it calculates screen mapping coordinates and displays an expanding spiderweb animation on top of the desktop.

## 2. What is the request flow?
1. **Startup**: The user runs `main.py` which instantiates a PyQt5 `QApplication`.
2. **Transparent Canvas**: The script gets desktop screen dimensions and launches `OverlayWindow` full-screen with transparent backgrounds, frameless styling, and click-through flags enabled.
3. **Camera Thread**: A background daemon thread starts the `camera_loop` function.
4. **Frame Processing**:
   - `camera_loop` opens the default camera.
   - `HandTracker` processes the frames to detect hand landmarks.
   - If landmarks are present:
     - The wrist location is identified, and coordinates are mapped from camera bounds to desktop monitor dimensions.
     - `GestureDetector` checks if the index (8) and pinky (20) fingers are extended and the middle (12) and ring (16) fingers are folded.
     - If yes and the 0.5s cooldown is passed, the thread emits the PyQt5 signal `trigger_web_signal(x, y)`.
5. **Animation Painting**:
   - The signal triggers `web_renderer.add_web(x, y)`.
   - `QTimer` refreshes the window updates every 30ms.
   - `WebRenderer` increments the web radius and fades the transparency (`alpha`).
   - `QPainter` paints 12 expanding lines (web spokes) and 5 concentric circles at the mapped desktop coordinates.
   - Terminate is triggered by hitting ESC in the camera view window.

## 3. Which packages are used and why?
- **`opencv-python` (`cv2`)**: Handles camera capturing, visual state overlays, and wait events.
- **`PyQt5`**: Provides transparent canvas layers, painting pipelines, custom events, and timing components.
- **`mediapipe`**: Computes hand landmarks and joints locations.
- **`math` (standard library)**: Evaluates distance formulas and trigonometric coordinates (`math.cos`, `math.sin`) for drawing webs.
- **`threading` (standard library)**: Runs camera capturing concurrently without blocking the PyQt5 main GUI loop.

## 4. Where does the data come from?
The input data comes from live video frames captured via the user's camera.

## 5. Where is the data stored?
All evaluations and frames are processed dynamically in RAM. No persistent files or databases are saved.

## 6. What is the role of the LLM?
There is **no LLM model used** in this project. The system relies entirely on standard computer vision regression models and geometry rules.

## 7. What breaks if the LLM is removed?
**Nothing breaks**, since the project has no AI language model dependencies.
