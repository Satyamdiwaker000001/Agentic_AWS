import warnings
# Suppress protobuf / mediapipe SymbolDatabase deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*SymbolDatabase.GetPrototype.*")

try:
    import cv2
except ImportError:
    cv2 = None
    print("[WARNING] cv2 (OpenCV) is missing. Hand tracking features will be offline. Install via 'pip install opencv-python'.")

try:
    import mediapipe as mp
except ImportError:
    mp = None
    print("[WARNING] mediapipe is missing. Hand tracking features will be offline. Install via 'pip install mediapipe'.")

class HandTracker:
    def __init__(self):
        if mp is not None:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                max_num_hands=2,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.7
            )
            self.drawer = mp.solutions.drawing_utils
        else:
            self.mp_hands = None
            self.hands = None
            self.drawer = None
        self.results = None

    def find_hands(self, frame):
        if cv2 is None or mp is None or self.hands is None:
            return frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                self.drawer.draw_landmarks(
                    frame,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame

    def get_landmarks(self, frame):
        landmarks = []
        if self.results and self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            h, w, _ = frame.shape
            for idx, lm in enumerate(hand.landmark):
                cx = int(lm.x * w)
                cy = int(lm.y * h)
                landmarks.append([idx, cx, cy])
        return landmarks

    def get_multi_hand_landmarks(self, frame):
        """
        Returns a list of dictionaries containing landmarks and labels for all detected hands.
        """
        all_hands = []
        if self.results and self.results.multi_hand_landmarks:
            h, w, _ = frame.shape
            for idx, hand in enumerate(self.results.multi_hand_landmarks):
                landmarks = []
                for lm_idx, lm in enumerate(hand.landmark):
                    cx = int(lm.x * w)
                    cy = int(lm.y * h)
                    landmarks.append([lm_idx, cx, cy])
                
                # Get label classification (Left/Right)
                label = "Right"  # Default fallback
                if self.results.multi_handedness:
                    try:
                        # MediaPipe classifications label handedness relative to the camera image
                        label = self.results.multi_handedness[idx].classification[0].label
                    except Exception:
                        pass
                
                all_hands.append({
                    "landmarks": landmarks,
                    "label": label
                })
        return all_hands


