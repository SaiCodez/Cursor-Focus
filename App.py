import sys
import keyboard

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QCursor
from PyQt6.QtWidgets import QApplication, QWidget


class CursorHighlighter(QWidget):
    def __init__(self):
        super().__init__()

        self.circle_size = 80

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.resize(self.circle_size, self.circle_size)

        self.follow_timer = QTimer()
        self.follow_timer.timeout.connect(self.update_position)
        self.follow_timer.start(16)

        self.hide()

    def update_position(self):
        pos = QCursor.pos()

        self.move(
            pos.x() - self.circle_size // 2,
            pos.y() - self.circle_size // 2
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(QColor(255, 255, 0, 255))
        pen.setWidth(5)

        painter.setPen(pen)
        painter.drawEllipse(5, 5, 70, 70)

    def show_for_five_seconds(self):
        self.show()

        QTimer.singleShot(
            5000,
            lambda: self.hide()
        )


app = QApplication(sys.argv)

window = CursorHighlighter()


def trigger():
    # Schedule the Qt action on the Qt event loop
    QTimer.singleShot(0, window.show_for_five_seconds)


keyboard.add_hotkey(
    "ctrl+shift+alt+z",
    trigger
)

sys.exit(app.exec())