import csv
import os
from datetime import datetime

LOG_FOLDER = "data_logs"
LIVE_FILE = "log.csv"
current_session_file = ""

def initialize_storage():
    global current_session_file
    if not os.path.exists(LOG_FOLDER): os.makedirs(LOG_FOLDER)
    if os.path.exists(LIVE_FILE): os.remove(LIVE_FILE)
    
    # Session filename remains date-based for easy sorting
    session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    current_session_file = os.path.join(LOG_FOLDER, f"session_{session_id}.csv")
    
    with open(current_session_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Score"])

def save_entry(score):
    # This creates a standard format: 2026-02-21 21:45:02
    full_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save to Archive
    if current_session_file:
        with open(current_session_file, 'a', newline='') as f:
            csv.writer(f).writerow([full_timestamp, score])

    # Save to Live (Keep this just Time for the Graph's X-axis clarity)
    with open(LIVE_FILE, 'a', newline='') as f:
        csv.writer(f).writerow([datetime.now().strftime("%H:%M:%S"), score])