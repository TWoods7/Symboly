import sys
import os
from datetime import datetime
import threading # Use threading for simplicity with your existing logic
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from Recorder import AlertnessRecorder # Import our new class

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.recorder_instance = AlertnessRecorder()
        self.recorder_thread = None

        # Window Setup
        self.setWindowTitle("Symboly Overlay")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint )# | Qt.WindowType.FramelessWindowHint
        self.setWindowOpacity(0.67) # Sets transparency for the WHOLE window (0.0 to 1.0)
        self.setStyleSheet("background-color: #262626;") # A dark base color
        self.setGeometry(100, 100, 800, 500)

        layout = QVBoxLayout(self)
        # --- Controls Layout ---
        controls = QHBoxLayout()
        
        self.btn_start = QPushButton("▶ Start")
        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_stop = QPushButton("⏹ Stop")
        
        # Style buttons
        style = "QPushButton { background: #222; color: white; padding: 8px; border-radius: 4px; } QPushButton:disabled { color: #555; }"
        for b in [self.btn_start, self.btn_pause, self.btn_stop]:
            b.setStyleSheet(style)
            controls.addWidget(b)

        self.btn_pause.setEnabled(False)
        self.btn_stop.setEnabled(False)

        # Connect signals
        self.btn_start.clicked.connect(self.start_recording)
        self.btn_pause.clicked.connect(self.pause_recording)
        self.btn_stop.clicked.connect(self.stop_recording)

        layout.addLayout(controls)

        # --- Browser ---
        self.browser = QWebEngineView()
        self.browser.page().setBackgroundColor(Qt.GlobalColor.transparent)
        self.browser.setUrl(QUrl("http://127.0.0.1:8050"))
        layout.addWidget(self.browser)

    def save_snapshot(self):
        """Captures the current state of the graph and saves it to the graphs folder."""
        folder = "graphs"
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Create timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(folder, f"graph_summary_{timestamp}.png")
        
        # Take the screenshot of the widget
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId())
        screenshot.save(file_path, "png")
        print(f"📈 Graph summary saved to {file_path}")

    def start_recording(self):
        if not self.recorder_thread or not self.recorder_thread.is_alive():
            self.recorder_thread = threading.Thread(target=self.recorder_instance.run, daemon=True)
            self.recorder_thread.start()
            self.btn_start.setEnabled(False)
            self.btn_pause.setEnabled(True)
            self.btn_stop.setEnabled(True)

    def pause_recording(self):
        is_paused = self.recorder_instance.toggle_pause()
        self.btn_pause.setText("▶ Resume" if is_paused else "⏸ Pause")

    def stop_recording(self):
        self.recorder_instance.stop()
        self.btn_start.setEnabled(True)
        self.btn_pause.setEnabled(False)
        self.btn_stop.setEnabled(False)
        self.btn_pause.setText("⏸ Pause")

    def closeEvent(self, event):
        """Triggers when you close the window manually."""
        self.save_snapshot()
        event.accept()

    # Mouse events for dragging...
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Overlay()
    window.show()
    sys.exit(app.exec())
