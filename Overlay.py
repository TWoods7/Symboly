import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
# This code creates a transparent overlay window using PyQt6. The window is frameless 
# and stays on top of other windows. It contains a label with some text, and the user 
# can click and drag the overlay to move it around the screen.

class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setGeometry(100, 100, 400, 200)

        # Label
        label = QLabel("This is a PyQt Transparent Overlay", self)
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: white;")
        label.adjustSize()
        label.move(40, 80)
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    sys.exit(app.exec())