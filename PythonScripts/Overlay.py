from operator import index
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import threading # Use threading for simplicity with your existing logic
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox)
from PyQt6.QtCore import Qt, QUrl, QPoint
from PyQt6.QtWebEngineWidgets import QWebEngineView
from Recorder import AlertnessRecorder
from pygrabber.dshow_graph import FilterGraph

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.recorder_instance = AlertnessRecorder()
        self.recorder_thread = None
        self.drag_pos = QPoint() # Initialize drag position

        # Window Setup
        self.setWindowTitle("Symboly Overlay")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowOpacity(0.67) # Sets transparency for the WHOLE window (0.0 to 1.0)
        self.setStyleSheet("background-color: #1a1a1a;")
        self.setGeometry(100, 100, 800, 500)
        
        layout = QVBoxLayout(self)
        # These three lines ensure the content touches the window edges
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Controls Layout ---
        controls = QHBoxLayout()
        # Add a little internal padding to the buttons so they don't touch the top edge
        controls.setContentsMargins(0, 0, 0, 0)
        
        # 1. Mode Selector (Self vs Others)
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Self (Webcam)", "Others (Screen)"])
        self.mode_selector.currentTextChanged.connect(self.change_mode)
        controls.addWidget(self.mode_selector)
        self.camera_selector = QComboBox()
        # Get actual camera names
        try:
            devices = FilterGraph().get_input_devices()
            # devices is a list of strings like ["Integrated Camera", "OBS Virtual Camera"]
            self.camera_selector.addItems(devices)
        except Exception as e:
            # Fallback if pygrabber fails
            self.camera_selector.addItems(["Camera 0"])#,"Camera 1", "Camera 2"
            
        self.camera_selector.currentIndexChanged.connect(self.change_camera)
        controls.addWidget(self.camera_selector)

        self.btn_start = QPushButton("▶ Start")
        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_stop = QPushButton("⏹ Stop")

        style = "QPushButton { background: #222; color: white; padding: 6px; border: 1px solid #444; } QPushButton:hover { background: #333; }"
        for b in [self.btn_start, self.btn_pause, self.btn_stop, self.mode_selector, self.camera_selector]:
            b.setStyleSheet(style)
            if isinstance(b, QPushButton): controls.addWidget(b)

        self.btn_start.clicked.connect(self.start_recording)
        self.btn_stop.clicked.connect(self.stop_recording)
        self.btn_pause.clicked.connect(self.pause_recording)

        self.btn_pause.setEnabled(False) # Start disabled until 'Start' is pressed
        self.btn_stop.setEnabled(False) # Start disabled until 'Start' is pressed
        layout.addLayout(controls)

        # --- Browser ---
        self.browser = QWebEngineView()
        # Ensure the browser itself doesn't have a background causing a "seam"
        self.browser.setContentsMargins(0, 0, 0, 0)
        # Kill the internal border of the browser widget
        self.browser.setStyleSheet("border: none; margin: -1px")
        
        self.browser.page().setBackgroundColor(Qt.GlobalColor.transparent)
        self.browser.setUrl(QUrl("http://127.0.0.1:8050"))

        layout.addWidget(self.browser)

    def change_mode(self, text):
        self.recorder_instance.mode = "Hardware" if "Self" in text else "Screen"

    def change_camera(self, index):
        self.recorder_instance.camera_index = index

    def save_snapshot(self):
            folder = "graphs"
            # Uses the live log file which contains the full current session
            log_path = "Live Data/log.csv" # Ensure this path matches your Data.py
            
            if not os.path.exists(folder): 
                os.makedirs(folder)
                
            if not os.path.exists(log_path):
                print("⚠️ No log data found to save.")
                return

            try:
                # 1. Load the data
                df = pd.read_csv(log_path, names=['Time', 'Score'])
                if df.empty: return

                # 2. Setup the Plot (Midnight Black Theme)
                plt.style.use('dark_background')
                fig, ax = plt.subplots(figsize=(12, 6))
                
                # 3. Plot the data
                ax.plot(df['Time'], df['Score'], color="#8e5ef6", linewidth=2, label='Alertness')
                
                # 4. Styling the "Full Session" Graph
                ax.set_title("SESSION ALERTNESS SUMMARY", fontsize=16, pad=20)#color='white'
                ax.set_xlabel("Session Timeline", fontsize=12)
                ax.set_ylabel("Alertness Score/Level", fontsize=12)
                ax.set_ylim(0, 11)                                            
                
               # Clean up the X-axis (shows fewer labels so they don't overlap)
                n = len(df)
                if n > 10:
                    ax.set_xticks(df['Time'][::n//10]) # Show about 10 timestamps
                
                plt.xticks(rotation=45)
                plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
                plt.tight_layout()

                # 5. Save with a high DPI for clarity
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                file_path = os.path.join(folder, f"full_session_{timestamp}.png")
                plt.savefig(file_path, dpi=300)
                plt.close() # Free up memory
                
                print(f"✅ Full session graph saved to: {file_path}")

            except Exception as e:
                print(f"❌ Could not save full session graph: {e}")

    def start_recording(self):
        if not self.recorder_thread or not self.recorder_thread.is_alive():
            self.camera_selector.setEnabled(False)
            self.mode_selector.setEnabled(False)
            
            self.recorder_thread = threading.Thread(target=self.recorder_instance.run, daemon=True)
            self.recorder_thread.start()

            self.btn_start.setEnabled(False)
            self.btn_pause.setEnabled(True)
            self.btn_stop.setEnabled(True)

    def pause_recording(self):
        is_paused = self.recorder_instance.toggle_pause()
        self.btn_pause.setText("▶ Resume" if is_paused else "⏸ Pause")

    def stop_recording(self):
        # NEW: Save the full session graph the moment STOP is pressed
        self.save_snapshot()
        self.recorder_instance.stop()
        
        self.btn_start.setEnabled(True)   
        self.btn_pause.setEnabled(False)
        self.btn_stop.setEnabled(False)

        self.camera_selector.setEnabled(True)
        self.mode_selector.setEnabled(True)

    def closeEvent(self, event):
        #"""Triggers when you close the window manually."""
        self.save_snapshot()
        event.accept()

    # Mouse events for dragging...
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # globalPosition().toPoint() works for PyQt6 coordinate systems
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            # Calculate how far the mouse has moved since the last frame
            diff = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.pos() + diff)
            self.drag_pos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Overlay()
    window.show()
    sys.exit(app.exec())
