import math

class GestureDetector:
    def __init__(self):
        pass

    def is_spiderman_gesture(self, landmarks):
        if not landmarks or len(landmarks) < 21:
            return False
            
        def dist(p1, p2):
            return math.hypot(p1[1]-p2[1], p1[2]-p2[2])
            
        wrist = landmarks[0]
        
        def is_finger_extended(tip_idx):
            return dist(landmarks[tip_idx], wrist) > dist(landmarks[tip_idx - 2], wrist)
            
        is_index_extended = is_finger_extended(8)
        is_middle_extended = is_finger_extended(12)
        is_ring_extended = is_finger_extended(16)
        is_pinky_extended = is_finger_extended(20)
        
        if is_index_extended and not is_middle_extended and not is_ring_extended and is_pinky_extended:
            return True
            
        return False
