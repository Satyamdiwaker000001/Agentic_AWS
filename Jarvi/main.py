import warnings
warnings.filterwarnings("ignore")

import os
import sys

# Suppress TensorFlow and MediaPipe internal C++ logging warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['GLOG_minloglevel'] = '3'


try:
    import cv2
except ImportError:
    cv2 = None
    print("[WARNING] cv2 (OpenCV) is missing. Camera processing will be offline.")

import time
import pyautogui
import pygetwindow as gw

from hand_tracker import HandTracker
from gesture_engine import GestureEngine
from file_manager import FileManager
from hud_renderer import HUDRenderer
from voice_engine import VoiceEngine

class MainApp:
    def __init__(self):
        print("[SYS] Booting JARVIS Core Interface...", flush=True)
        time.sleep(0.15)
        print("[SYS] Calibrating hand gesture landmarks model...", flush=True)
        self.tracker = HandTracker()
        
        print("[SYS] Initializing system cursor mapping coordinate matrix...", flush=True)
        self.gesture_engine = GestureEngine(click_threshold=35, smooth_factor=5)
        self.file_manager = FileManager()
        self.hud = HUDRenderer()
        
        print("[SYS] Spawning asynchronous voice detection pipeline...", flush=True)
        self.voice_engine = VoiceEngine(self)
        
        self.running = True
        self.window_title = "JARVI File Core OS"
        pyautogui.FAILSAFE = False  # Allows moving the cursor to corners without raising exceptions
        
    def stop(self):
        print("[JARVI] Deactivating systems...", flush=True)
        self.running = False
        if self.voice_engine:
            self.voice_engine.running = False

    def minimize_window(self):
        try:
            win = gw.getWindowsWithTitle(self.window_title)
            if win:
                win[0].minimize()
            else:
                print(f"[JARVI] Window with title '{self.window_title}' not found to minimize.", flush=True)
        except Exception as e:
            print(f"[JARVI] Error minimizing window: {e}", flush=True)

    def restore_window(self):
        try:
            win = gw.getWindowsWithTitle(self.window_title)
            if win:
                win[0].restore()
                win[0].activate()
            else:
                print(f"[JARVI] Window with title '{self.window_title}' not found to restore.", flush=True)
        except Exception as e:
            print(f"[JARVI] Error restoring window: {e}", flush=True)

    def search_and_run_file(self, filename):
        print(f"[JARVI] Performing A: drive query: '{filename}'", flush=True)
        success, path = self.file_manager.search_and_execute_file(filename)
        if success:
            self.voice_engine.speak(f"Successfully launched {os.path.basename(path)}.")
        else:
            self.voice_engine.speak(f"I could not execute {filename}. {path}")

    def run(self):
        cap = None
        if cv2 is not None:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cap.isOpened():
                print("[WARNING] Webcam access failed. Operating in voice-only headless mode.", flush=True)
                cap = None
            else:
                print("[SYS] Webcam connection established successfully.", flush=True)
        else:
            print("[WARNING] OpenCV not installed. Operating in voice-only headless mode.", flush=True)

        # Start background voice listener thread
        self.voice_engine.start()


        pinch_released = True
        fist_released = True
        offset = 0
        scroll_last_time = 0
        scroll_cooldown = 0.25
        
        screen_w, screen_h = pyautogui.size()

        print("\n============================================================", flush=True)
        print("             J.A.R.V.I.S.  SYSTEM  ACTIVE  v5.0             ", flush=True)
        print("============================================================", flush=True)
        print(f" [Monitor Grid] Resolved resolution: {screen_w}x{screen_h}", flush=True)
        print(" [Wake Protocol] Address voice commands with: 'Jarvis' or 'Jarvi'", flush=True)
        print(" [Hand Gestures] Index tracking = Cursor, Pinch = Click, Fist = Back", flush=True)
        print(" [A: drive File Explorer] Recursive search engine enabled", flush=True)
        print("============================================================\n", flush=True)



        while self.running:
            if cap is not None:
                success, frame = cap.read()
                if not success:
                    time.sleep(0.03)
                    continue

                frame = cv2.flip(frame, 1)
                cam_h, cam_w, _ = frame.shape
                if cam_w == 0 or cam_h == 0:
                    cam_w, cam_h = 640, 480

                # Process hand tracking landmarks
                frame = self.tracker.find_hands(frame)
                detected_hands = self.tracker.get_multi_hand_landmarks(frame)

                gesture_state = "NO_HAND"
                cursor_pos_hud = None
                hovered_idx = -1

                all_items = self.file_manager.list_contents()
                visible_items = all_items[offset:offset + 11]

                # Dual hand tracking logic:
                # If two hands are detected:
                #   - We sort hands by their horizontal x-coordinate (using the wrist landmark 0).
                #   - The hand on the left (smaller x) is mapped to left_hand_lms (fist/back navigation).
                #   - The hand on the right (larger x) is mapped to right_hand_lms (cursor/click controls).
                # If a single hand is detected, it acts as the default fallback for all controls.
                right_hand_lms = None
                left_hand_lms = None

                if len(detected_hands) == 1:
                    right_hand_lms = detected_hands[0]["landmarks"]
                    left_hand_lms = detected_hands[0]["landmarks"]
                elif len(detected_hands) >= 2:
                    # Sort hands by wrist x-coordinate: landmark index 0 is wrist, its cx is index 1
                    try:
                        sorted_hands = sorted(detected_hands, key=lambda h: h["landmarks"][0][1])
                        left_hand_lms = sorted_hands[0]["landmarks"]
                        right_hand_lms = sorted_hands[1]["landmarks"]
                    except Exception as e:
                        print(f"[JARVI] Error sorting hands: {e}")
                        right_hand_lms = detected_hands[0]["landmarks"]
                        left_hand_lms = detected_hands[0]["landmarks"]


                # 1. Right Hand Cursor mapping & Click Execution
                if right_hand_lms:
                    r_gesture, r_tip = self.gesture_engine.detect_gesture(right_hand_lms)
                    gesture_state = r_gesture
                    
                    if r_tip:
                        cx, cy = r_tip[1], r_tip[2]
                        
                        raw_x = int((cx / cam_w) * screen_w)
                        raw_y = int((cy / cam_h) * screen_h)
                        
                        smoothed = self.gesture_engine.get_smoothed_position((raw_x, raw_y))
                        if smoothed:
                            sx, sy = smoothed
                            pyautogui.moveTo(sx, sy)
                            
                            mapped_hud_x = int((cx / cam_w) * 1280)
                            mapped_hud_y = int((cy / cam_h) * 720)
                            cursor_pos_hud = (mapped_hud_x, mapped_hud_y)
                            
                            if 660 <= mapped_hud_x <= 1250:
                                if 225 <= mapped_hud_y <= 665:
                                    hovered_idx = (mapped_hud_y - 225) // 40
                                    if hovered_idx >= len(visible_items):
                                        hovered_idx = -1
                                        
                                # HUD List scrolling check
                                current_time = time.time()
                                if current_time - scroll_last_time > scroll_cooldown:
                                    if 170 <= mapped_hud_y < 225:
                                        if offset > 0:
                                            offset -= 1
                                            scroll_last_time = current_time
                                    elif 665 < mapped_hud_y <= 710:
                                        if offset + 11 < len(all_items):
                                            offset += 1
                                            scroll_last_time = current_time

                    if gesture_state == "CLICK" and pinch_released:
                         pinch_released = False
                         pyautogui.click()
                         if hovered_idx != -1:
                             selected_item = visible_items[hovered_idx]
                             if selected_item["is_dir"]:
                                 self.file_manager.navigate_to(selected_item["name"])
                                 offset = 0
                             else:
                                 self.file_manager.open_file(selected_item["path"])
                    elif gesture_state == "HOVER":
                         pinch_released = True
                else:
                    pinch_released = True

                # 2. Left Hand Back navigation execution
                if left_hand_lms:
                    l_gesture, _ = self.gesture_engine.detect_gesture(left_hand_lms)
                    if l_gesture == "FIST" and fist_released:
                         fist_released = False
                         pyautogui.hotkey('alt', 'left')
                         self.file_manager.navigate_up()
                         offset = 0
                    elif l_gesture != "FIST":
                         fist_released = True
                else:
                    fist_released = True


                # Compile final HUD visual layer
                hud_frame = self.hud.draw_hud(
                    camera_frame=frame,
                    current_dir=self.file_manager.get_current_directory(),
                    items=visible_items,
                    hovered_idx=hovered_idx,
                    gesture_state=gesture_state,
                    cursor_pos=cursor_pos_hud
                )

                # Check if camera GUI window has been minimized
                is_window_minimized = False
                try:
                    win = gw.getWindowsWithTitle(self.window_title)
                    if win and win[0].isMinimized:
                        is_window_minimized = True
                except Exception:
                    pass

                # If not minimized, show HUD. Otherwise keep background process ticking.
                if not is_window_minimized and hud_frame is not None:
                    cv2.imshow(self.window_title, hud_frame)
                    # Check for ESC key escape
                    if cv2.waitKey(1) & 0xFF == 27:
                        self.stop()
                        break
                else:
                    # Maintain OpenCV event loop ticking so background tasks remain alive
                    cv2.waitKey(1)
            else:
                # Running headless (voice-only mode)
                time.sleep(0.05)

        if cap is not None:
            cap.release()
        if cv2 is not None:
            cv2.destroyAllWindows()
        print("[JARVI] Session successfully terminated.")

def main():
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()
