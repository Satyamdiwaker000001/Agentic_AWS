import math

class GestureEngine:
    def __init__(self, click_threshold=35, smooth_factor=5):
        self.click_threshold = click_threshold
        self.history = []
        self.smooth_factor = smooth_factor

    def get_smoothed_position(self, pos):
        if not pos:
            return None
        self.history.append(pos)
        if len(self.history) > self.smooth_factor:
            self.history.pop(0)
        xs = [p[0] for p in self.history]
        ys = [p[1] for p in self.history]
        return (sum(xs) // len(xs), sum(ys) // len(ys))


    def calculate_distance(self, p1, p2):
        return math.hypot(p2[1] - p1[1], p2[2] - p1[2])

    def detect_gesture(self, landmarks):
        if not landmarks or len(landmarks) < 21:
            return "NO_HAND", None

        # Landmarks indices:
        # 0: Wrist, 4: Thumb Tip, 8: Index Tip, 12: Middle Tip, 16: Ring Tip, 20: Pinky Tip
        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]

        # 1. Check for Fist (Go Back)
        # Verify if all 4 main fingers are folded (tip is closer to wrist than joint)
        is_index_folded = self.calculate_distance(index_tip, wrist) < self.calculate_distance(landmarks[6], wrist)
        is_middle_folded = self.calculate_distance(middle_tip, wrist) < self.calculate_distance(landmarks[10], wrist)
        is_ring_folded = self.calculate_distance(ring_tip, wrist) < self.calculate_distance(landmarks[14], wrist)
        is_pinky_folded = self.calculate_distance(pinky_tip, wrist) < self.calculate_distance(landmarks[18], wrist)

        if is_index_folded and is_middle_folded and is_ring_folded and is_pinky_folded:
            return "FIST", index_tip

        # 2. Check for Click (Pinch gesture: Thumb Tip + Index Tip close)
        click_dist = self.calculate_distance(thumb_tip, index_tip)
        if click_dist < self.click_threshold:
            return "CLICK", index_tip

        # 3. Default state: Hover/Cursor control
        return "HOVER", index_tip
