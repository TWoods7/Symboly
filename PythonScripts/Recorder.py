import pyautogui
import time
import os
from datetime import datetime
from Emotion import get_alertness_score
from Data import initialize_storage, save_entry

class AlertnessRecorder:
    def __init__(self):
        self.running = False
        self.paused = False
        self.CAPTURE_INTERVAL = 0.5  # Seconds between captures
        self.SCREENSHOT_BASE_FOLDER = "screenshots"

    def run(self):
        initialize_storage()
        session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        current_session_folder = os.path.join(self.SCREENSHOT_BASE_FOLDER, session_id)
        
        if not os.path.exists(current_session_folder):
            os.makedirs(current_session_folder)

        print(f"🚀 Recorder Started.")
        print(f"📁 Session Folder: {current_session_folder}")
        print(f"⏱️  Interval: {self.CAPTURE_INTERVAL}s")
        print("---------------------------------------------")

        try:
            self.running = True
            while self.running:
                if not self.paused:
                    screenshot = pyautogui.screenshot()
                    score = get_alertness_score(screenshot)
                    save_entry(score)
                    
                    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_name = f"{timestamp_str}_score_{score}.png"
                    screenshot.save(os.path.join(current_session_folder, file_name))
                    print(f"Recorded Score: {score}")
                
                time.sleep(self.CAPTURE_INTERVAL)

        except KeyboardInterrupt:
            print("\n👋 Recorder stopped by user.")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
    
    def stop(self):
            self.running = False

    def toggle_pause(self):
            self.paused = not self.paused
            return self.paused
