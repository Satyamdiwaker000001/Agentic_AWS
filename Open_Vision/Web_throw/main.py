import sys
import cv2
import threading
import time
from PyQt5.QtWidgets import QApplication

from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from overlay_window import OverlayWindow
from utils import map_coordinates

def camera_loop(overlay, dest_w, dest_h):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    tracker = HandTracker()
    detector = GestureDetector()
    
    last_trigger_time = 0
    cooldown = 0.5
    
    while True:
        success, frame = cap.read()
        if not success:
            break
            
        frame = tracker.find_hands(frame)
        landmarks = tracker.get_landmarks(frame)
        
        if landmarks:
            wrist_x, wrist_y = landmarks[0][1], landmarks[0][2]
            
            src_h, src_w, _ = frame.shape
            mapped_x, mapped_y = map_coordinates(wrist_x, wrist_y, src_w, src_h, dest_w, dest_h)
            
            is_spidey = detector.is_spiderman_gesture(landmarks)
            
            current_time = time.time()
            if is_spidey and (current_time - last_trigger_time > cooldown):
                overlay.trigger_web_signal.emit(mapped_x, mapped_y)
                last_trigger_time = current_time

            cv2.putText(frame, "Spidey Gesture: " + str(is_spidey), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if is_spidey else (0, 0, 255), 2)
            
        cv2.imshow("Web Throw Cam", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
            
    cap.release()
    cv2.destroyAllWindows()
    QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    screen = app.primaryScreen().geometry()
    dest_w, dest_h = screen.width(), screen.height()
    
    overlay = OverlayWindow()
    overlay.show()
    
    cam_thread = threading.Thread(target=camera_loop, args=(overlay, dest_w, dest_h), daemon=True)
    cam_thread.start()
    
    sys.exit(app.exec_())
