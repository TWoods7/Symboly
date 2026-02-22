import pyautogui
import time
import os
from datetime import datetime
from Emotion import get_alertness_score
from Data import initialize_storage, save_entry

# --- Configuration ---
SCREENSHOT_BASE_FOLDER = "screenshots"
CAPTURE_INTERVAL = 3  # Seconds between captures

def start_recording():
    # 1. Initialize files via Data.py
    # This clears the live log and sets up the session CSV in data_logs/
    initialize_storage()

    # 2. Setup a unique folder for this session's screenshots
    session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    current_session_folder = os.path.join(SCREENSHOT_BASE_FOLDER, session_id)
    
    if not os.path.exists(current_session_folder):
        os.makedirs(current_session_folder)

    print(f"🚀 Recorder Started.")
    print(f"📁 Session Folder: {current_session_folder}")
    print(f"⏱️  Interval: {CAPTURE_INTERVAL}s")
    print("---------------------------------------------")

    try:
        while True:
            # 3. Capture the screen
            # Note: MediaPipe in Emotion.py will analyze this image
            screenshot = pyautogui.screenshot()
            
            # 4. Get AI Alertness Score (1-10) from Emotion.py
            score = get_alertness_score(screenshot)
            
            # 5. Log numerical data via Data.py
            # This saves to both 'log.csv' (live) and 'data_logs/session_...csv' (archive)
            save_entry(score)
            
            # 6. Save the screenshot with a clean timestamp
            # Format: YYYYMMDD_HHMMSS_score_X.png (Perfect for chronological sorting)
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{timestamp_str}_score_{score}.png"
            file_path = os.path.join(current_session_folder, file_name)
            
            screenshot.save(file_path)
            
            # 7. Console feedback
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Score: {score}/10 | Saved: {file_name}")
            
            # Wait for next interval
            time.sleep(CAPTURE_INTERVAL)

    except KeyboardInterrupt:
        print("\n👋 Recorder stopped by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    start_recording()





# import pyautogui
# import time
# import os
# from datetime import datetime
# from Emotion import get_alertness_score # Import your AI logic
# import csv

# # This script continuously takes screenshots of the user's screen at a specified interval 
# # and saves them to a designated folder.

# # --- CONFIGURATION ---
# SAVE_FOLDER = "PythonScripts/screenshots"
# INTERVAL = 3  # seconds
# # ---------------------

# def start_recording():
#     # Create the folder if it doesn't exist
#     if not os.path.exists(SAVE_FOLDER):
#         os.makedirs(SAVE_FOLDER)
#         print(f"Created folder: {SAVE_FOLDER}")

#     print(f"Recording started. Saving to '{SAVE_FOLDER}' every {INTERVAL}s.")
#     print("TO STOP: Move your mouse to the TOP-LEFT corner of your screen.")

#     try:
#         while True:
#             # 1. Capture the screenshot into a variable (RAM)
#             # This is the line you are adding/replacing
#             shot = pyautogui.screenshot()

#             # 2. Analyze the screenshot using your Emotion script
#             # This is the "Bridge" to your AI
#             score = get_alertness_score(shot)

#             # 3. Generate the filename
#             timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             # We add the score to the filename so you can verify the AI later
#             file_name = f"alert_{score}_{timestamp}.png"
#             file_path = os.path.join(SAVE_FOLDER, file_name)

#             # 4. Save the screenshot to the hard drive
#             shot.save(file_path)

#             # 5. Log the data for Graph.py (Shared CSV)
#             with open('log.csv', 'a', newline='') as f:
#                 import csv
#                 writer = csv.writer(f)
#                 writer.writerow([datetime.now().strftime("%H:%M:%S"), score])
            
#             print(f"[{timestamp}] Score: {score}/10 | Saved: {file_name}")
            
#             # Wait for the next interval
#             time.sleep(INTERVAL)

#     except pyautogui.FailSafeException:
#         print("\nFail-safe triggered from mouse movement. Recording stopped.")
#     except KeyboardInterrupt:
#         print("\nManual stop detected. Recording stopped.")

# if __name__ == "__main__":
#     start_recording()