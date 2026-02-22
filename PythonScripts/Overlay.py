import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symboly Overlay")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(100, 100, 800, 500)

        layout = QVBoxLayout(self)
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



# from PyQt6.QtWidgets import QApplication, QWidget, QLabel
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont
# # This code creates a transparent overlay window using PyQt6. The window is frameless 
# # and stays on top of other windows. It contains a label with some text, and the user 
# # can click and drag the overlay to move it around the screen.

# class Overlay(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Window setup
#         self.setWindowFlags(
#             #Qt.WindowType.FramelessWindowHint |
#             Qt.WindowType.WindowStaysOnTopHint
#         )

#         self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

#         self.setGeometry(100, 100, 400, 200)

#         # Label
#         label = QLabel("This is a PyQt Transparent Overlay", self)
#         label.setFont(QFont("Arial", 16))
#         label.setStyleSheet("color: white;")
#         label.adjustSize()
#         label.move(40, 80)
#     def mousePressEvent(self, event):
#         if event.button() == Qt.MouseButton.LeftButton:
#             self.drag_pos = event.globalPosition().toPoint()

#     def mouseMoveEvent(self, event):
#         if event.buttons() == Qt.MouseButton.LeftButton:
#             self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
#             self.drag_pos = event.globalPosition().toPoint()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     overlay = Overlay()
#     overlay.show()
#     sys.exit(app.exec())