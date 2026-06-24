try:
    import cv2
except ImportError:
    cv2 = None
    print("[WARNING] cv2 (OpenCV) is missing. HUD Renderer will be offline.")

import numpy as np
import time

try:
    import psutil
except ImportError:
    psutil = None


class HUDRenderer:
    def __init__(self):
        # High-tech Holographic Colors (BGR Format)
        self.color_cyan = (255, 200, 50)
        self.color_glow = (255, 230, 120)
        self.color_red = (50, 50, 255)
        self.color_green = (50, 255, 50)
        self.color_bg = (20, 15, 10)
        self.color_text = (240, 240, 240)
        
        self.prev_time = time.time()
        self.fps = 30

        self.scanline_y = 0
        self.pulse_radius = 5
        self.pulse_direction = 1

    def draw_hud(self, camera_frame, current_dir, items, hovered_idx, gesture_state, cursor_pos):
        """
        Synthesizes a combined 1280x720 Jarvis HUD display.
        camera_frame: cv2 raw capture (usually 640x480 or similar)
        """
        if cv2 is None:
            return None
        # 1. Create a black canvas (1280 x 720)
        canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
        
        # 2. Resize and place camera frame on the left half (640 x 720)
        cam_h, cam_w, _ = camera_frame.shape
        cam_resized = cv2.resize(camera_frame, (640, 720))
        canvas[0:720, 0:640] = cam_resized
        
        # Draw partition line
        cv2.line(canvas, (640, 0), (640, 720), self.color_cyan, 2)
        
        # 3. Draw Holographic background overlay on the right half (640 x 720)
        overlay = canvas.copy()
        cv2.rectangle(overlay, (642, 0), (1280, 720), self.color_bg, -1)
        # Apply semi-transparent glass effect
        cv2.addWeighted(overlay, 0.45, canvas, 0.55, 0, canvas)
        
        # 4. Render JARVIS Diagnostics & Stats (Holographic details)
        self.render_diagnostics(canvas, gesture_state, cursor_pos)
        
        # 5. Render File Explorer list
        self.render_file_explorer(canvas, current_dir, items, hovered_idx)
        
        # 6. Render Active Cursor Target
        self.render_cursor(canvas, cursor_pos, gesture_state)
        
        # 7. Render Glowing HUD Frames and Scanning Grid Lines
        self.render_hologram_frames(canvas)
        
        return canvas

    def render_diagnostics(self, canvas, gesture_state, cursor_pos):
        # Calculate live FPS using exponential moving average
        curr_time = time.time()
        time_diff = curr_time - self.prev_time
        if time_diff > 0:
            self.fps = int(0.9 * self.fps + 0.1 * (1.0 / time_diff))
        self.prev_time = curr_time

        # Title of Diagnostics Panel
        cv2.putText(canvas, "JARVIS SYSTEM CORE v5.0", (660, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.color_cyan, 2)
        cv2.putText(canvas, "DRIVE CONTROL HUD ACTIVE", (660, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.color_glow, 1)
        
        # Display current local clock in top corner
        local_clock = time.strftime("%Y-%m-%d  %H:%M:%S")
        cv2.putText(canvas, local_clock, (970, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.color_glow, 1)

        # Draw standard diagnostic box
        cv2.rectangle(canvas, (660, 80), (950, 160), self.color_cyan, 1)
        cv2.putText(canvas, f"GESTURE: {gesture_state}", (670, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.color_text, 1)
        
        # Position Coordinates
        pos_str = f"CURSOR: X={cursor_pos[0]}, Y={cursor_pos[1]}" if cursor_pos else "CURSOR: NO_HAND"
        cv2.putText(canvas, pos_str, (670, 118), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.color_glow, 1)

        # FPS indicator
        cv2.putText(canvas, f"FPS: {self.fps}", (670, 136), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.color_cyan, 1)

        # Fetch CPU & RAM load statistics
        cpu_val = 0
        ram_val = 0
        if psutil is not None:
            try:
                cpu_val = int(psutil.cpu_percent())
                ram_val = int(psutil.virtual_memory().percent)
            except Exception:
                pass

        # CPU Metric & mini progress bar
        cv2.putText(canvas, f"CPU: {cpu_val}%", (760, 136), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.color_text, 1)
        cv2.rectangle(canvas, (830, 129), (940, 135), (50, 50, 50), -1)
        w_cpu = int(110 * (cpu_val / 100.0))
        cv2.rectangle(canvas, (830, 129), (830 + w_cpu, 135), self.color_cyan, -1)

        # RAM Metric & mini progress bar
        cv2.putText(canvas, f"RAM: {ram_val}%", (760, 150), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.color_text, 1)
        cv2.rectangle(canvas, (830, 144), (940, 150), (50, 50, 50), -1)
        w_ram = int(110 * (ram_val / 100.0))
        cv2.rectangle(canvas, (830, 144), (830 + w_ram, 150), self.color_glow, -1)

        # Futuristic circular scanning radar graphic on top-right of HUD
        center_x, center_y = 1180, 120
        cv2.circle(canvas, (center_x, center_y), 40, self.color_cyan, 1)
        cv2.circle(canvas, (center_x, center_y), 25, self.color_glow, 1)
        cv2.circle(canvas, (center_x, center_y), 5, self.color_red if gesture_state == "CLICK" else self.color_cyan, -1)
        
        # Draw rotating scanning sweeps
        angle = int(time.time() * 3) % 360
        rad = np.radians(angle)
        end_x = int(center_x + 40 * np.cos(rad))
        end_y = int(center_y + 40 * np.sin(rad))
        cv2.line(canvas, (center_x, center_y), (end_x, end_y), self.color_glow, 1)


    def render_file_explorer(self, canvas, current_dir, items, hovered_idx):
        # Current Path Header
        cv2.putText(canvas, "DIRECTORY LOG:", (660, 175), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_cyan, 1)
        
        # Display directory path (truncate if too long)
        display_dir = current_dir
        if len(display_dir) > 55:
            display_dir = "..." + display_dir[-52:]
        cv2.putText(canvas, display_dir, (660, 195), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, self.color_text, 2)
        
        # Draw Explorer Box Border
        cv2.rectangle(canvas, (660, 210), (1250, 680), self.color_cyan, 1)
        
        # Draw Items List (limit to 10 lines max)
        list_y_start = 225
        item_height = 40
        
        if not items:
            cv2.putText(canvas, "[Folder is Empty]", (680, list_y_start + 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color_glow, 1)
            return

        for idx, item in enumerate(items[:11]):  # Max 11 items
            y_pos = list_y_start + (idx * item_height)
            
            # Hovered Item highlighting (glass highlight rectangle)
            if idx == hovered_idx:
                hl_overlay = canvas.copy()
                cv2.rectangle(hl_overlay, (665, y_pos), (1245, y_pos + item_height - 5), self.color_cyan, -1)
                cv2.addWeighted(hl_overlay, 0.25, canvas, 0.75, 0, canvas)
                # Draw border highlight
                cv2.rectangle(canvas, (665, y_pos), (1245, y_pos + item_height - 5), self.color_glow, 1)

            # Icon Prefix
            prefix = "DIR > " if item["is_dir"] else "FILE > "
            prefix_color = self.color_cyan if item["is_dir"] else self.color_glow
            
            # Draw Item Prefix
            cv2.putText(canvas, prefix, (680, y_pos + 25), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, prefix_color, 2)
            
            # Display item name (truncate if too long)
            item_name = item["name"]
            if len(item_name) > 40:
                item_name = item_name[:37] + "..."
                
            cv2.putText(canvas, item_name, (760, y_pos + 25), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, self.color_text, 1)

        # Draw a quick-reference operating manual bar at the bottom
        cv2.putText(canvas, "MANUAL: Right hand = Move Cursor | Pinch = Click | Left hand Fist = Go Back", (665, 705), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.color_glow, 1)


    def render_cursor(self, canvas, cursor_pos, gesture_state):
        if not cursor_pos:
            return

        cx, cy = cursor_pos
        # Limit cursor x to camera frame boundary if needed, but since it's mapped in main, we just draw
        
        # Color based on active gesture
        cursor_color = self.color_cyan
        if gesture_state == "CLICK":
            cursor_color = self.color_red
        elif gesture_state == "FIST":
            cursor_color = self.color_green
            
        # Draw high-tech HUD crosshair target on cursor location
        cv2.circle(canvas, (cx, cy), 15, cursor_color, 1)
        cv2.circle(canvas, (cx, cy), 3, cursor_color, -1)
        
        # Diagonal ticks
        cv2.line(canvas, (cx - 20, cy), (cx - 8, cy), cursor_color, 1)
        cv2.line(canvas, (cx + 8, cy), (cx + 20, cy), cursor_color, 1)
        cv2.line(canvas, (cx, cy - 20), (cx, cy - 8), cursor_color, 1)
        cv2.line(canvas, (cx, cy + 8), (cx, cy + 20), cursor_color, 1)

        # Pulse circle on clicked state
        if gesture_state == "CLICK":
            self.pulse_radius += self.pulse_direction * 2
            if self.pulse_radius > 35 or self.pulse_radius < 5:
                self.pulse_direction *= -1
            cv2.circle(canvas, (cx, cy), self.pulse_radius, self.color_glow, 2)

    def render_hologram_frames(self, canvas):
        # Vertical scanline animation moving across camera feed (left half)
        self.scanline_y += 4
        if self.scanline_y > 720:
            self.scanline_y = 0
            
        # Draw translucent scanning horizontal sweep line
        scanline_overlay = canvas.copy()
        cv2.line(scanline_overlay, (0, self.scanline_y), (640, self.scanline_y), self.color_glow, 2)
        cv2.addWeighted(scanline_overlay, 0.35, canvas, 0.65, 0, canvas)

        # Outer HUD border brackets
        h, w, _ = canvas.shape
        cv2.rectangle(canvas, (10, 10), (w - 10, h - 10), self.color_cyan, 1)
        
        # Corner brackets decoration
        offset = 30
        corner_len = 20
        # Top-Left
        cv2.line(canvas, (offset, offset), (offset + corner_len, offset), self.color_glow, 3)
        cv2.line(canvas, (offset, offset), (offset, offset + corner_len), self.color_glow, 3)
        # Top-Right
        cv2.line(canvas, (w - offset - corner_len, offset), (w - offset, offset), self.color_glow, 3)
        cv2.line(canvas, (w - offset, offset), (w - offset, offset + corner_len), self.color_glow, 3)
        # Bottom-Left
        cv2.line(canvas, (offset, h - offset), (offset + corner_len, h - offset), self.color_glow, 3)
        cv2.line(canvas, (offset, h - offset), (offset, h - offset - corner_len), self.color_glow, 3)
        # Bottom-Right
        cv2.line(canvas, (w - offset - corner_len, h - offset), (w - offset, h - offset), self.color_glow, 3)
        cv2.line(canvas, (w - offset, h - offset), (w - offset, h - offset - corner_len), self.color_glow, 3)
