import cv2
import time
import os
import pyautogui
import pygetwindow as gw
from PIL import Image  # FIX: This solves the 'Image is not defined' error
from Emotion import get_alertness_score
from Data import initialize_storage, save_entry

class AlertnessRecorder:
    def __init__(self):
        self.mode = "Hardware" # Default mode
        self.window_title = "Zoom"
        self.running = False
        self.paused = False
        self.CAPTURE_INTERVAL = 0.5  # Seconds between captures
        self.camera_index = 0  # Default webcam index (0 is usually the built-in webcam)

    def run(self):
        initialize_storage()
        cap = None
        
        try:
            self.running = True
            while self.running:
                if not self.paused:
                    if self.mode == "Hardware":
                        if cap is None or not cap.isOpened():
                            cap = cv2.VideoCapture(self.camera_index)
                        
                        ret, frame = cap.read()
                        if ret:
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            img = Image.fromarray(frame_rgb)
                        else: continue
                            
                    else: # Screen Capture Mode
                        if cap is not None: # Close camera if we switched modes
                            cap.release()
                            cap = None
                            
                        # Find window and take screenshot (your previous logic)
                        img = pyautogui.screenshot() # Simplified for example
                    
                    score = get_alertness_score(img)
                    save_entry(score)
                time.sleep(self.CAPTURE_INTERVAL)
        except Exception as e:
            print(f"❌ Recorder Error: {e}")
        finally:
            if cap: cap.release()
    
    def stop(self):
            self.running = False

    def toggle_pause(self):
            self.paused = not self.paused
            return self.paused
