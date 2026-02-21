import pyautogui
import time
import os
from datetime import datetime

# This script continuously takes screenshots of the user's screen at a specified interval 
# and saves them to a designated folder.

# --- CONFIGURATION ---
SAVE_FOLDER = "screenshots"
INTERVAL = 3  # seconds
# ---------------------

def start_recording():
    # Create the folder if it doesn't exist
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        print(f"Created folder: {SAVE_FOLDER}")

    print(f"Recording started. Saving to '{SAVE_FOLDER}' every {INTERVAL}s.")
    print("TO STOP: Move your mouse to the TOP-LEFT corner of your screen.")

    try:
        while True:
            # Generate a unique filename using the current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(SAVE_FOLDER, f"screenshot_{timestamp}.png")

            # Take and save the screenshot
            pyautogui.screenshot(file_path)
            
            print(f"Saved: {file_path}")
            
            # Wait for the next interval
            time.sleep(INTERVAL)

    except pyautogui.FailSafeException:
        print("\nFail-safe triggered from mouse movement. Recording stopped.")
    except KeyboardInterrupt:
        print("\nManual stop detected. Recording stopped.")

if __name__ == "__main__":
    start_recording()