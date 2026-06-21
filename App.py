import sys
import os
import json
import keyboard

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QCursor
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QColorDialog,
    QVBoxLayout,
    QLabel,
    QSlider,
)


class CursorHighlighter(QWidget):
    def __init__(self):
        super().__init__()

        self.circle_size = 80
        self.ring_color = QColor(255, 255, 0)

        self.setup_settings()
        self.log("Application starting")

        self.load_settings()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.resize(
            self.circle_size,
            self.circle_size
        )

        self.follow_timer = QTimer()
        self.follow_timer.timeout.connect(
            self.update_position
        )
        self.follow_timer.start(16)

        self.hide()

        self.log("CursorHighlighter initialized")

    def setup_settings(self):
        appdata = os.getenv("APPDATA")

        self.settings_dir = os.path.join(
            appdata,
            "CursorHighlighter"
        )

        os.makedirs(
            self.settings_dir,
            exist_ok=True
        )

        self.settings_file = os.path.join(
            self.settings_dir,
            "settings.json"
        )

        self.log_file = os.path.join(
            self.settings_dir,
            "debug.log"
        )

    def log(self, message):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except:
            pass

    def load_settings(self):
        try:
            self.log("Loading settings")

            if os.path.exists(self.settings_file):
                self.log("settings.json found")

                with open(
                    self.settings_file,
                    "r",
                    encoding="utf-8"
                ) as f:
                    data = json.load(f)

                self.circle_size = data.get(
                    "size",
                    80
                )

                color = data.get(
                    "color",
                    [255, 255, 0]
                )

                self.ring_color = QColor(
                    color[0],
                    color[1],
                    color[2]
                )

                self.log(
                    f"Loaded size={self.circle_size} color={color}"
                )

            else:
                self.log("settings.json not found")

        except Exception as e:
            self.log(f"LOAD ERROR: {e}")

    def save_settings(self):
        try:
            data = {
                "size": self.circle_size,
                "color": [
                    self.ring_color.red(),
                    self.ring_color.green(),
                    self.ring_color.blue()
                ]
            }

            with open(
                self.settings_file,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    data,
                    f,
                    indent=4
                )

            self.log(
                f"SAVED size={self.circle_size} color={data['color']}"
            )

        except Exception as e:
            self.log(f"SAVE ERROR: {e}")

    def update_position(self):
        pos = QCursor.pos()

        self.move(
            pos.x() - self.circle_size // 2,
            pos.y() - self.circle_size // 2
        )

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        pen = QPen(self.ring_color)
        pen.setWidth(5)

        painter.setPen(pen)

        margin = 5

        painter.drawEllipse(
            margin,
            margin,
            self.circle_size - margin * 2,
            self.circle_size - margin * 2
        )

    def show_for_five_seconds(self):
        self.log("Highlight triggered")

        self.show()

        QTimer.singleShot(
            5000,
            self.hide
        )

    def set_ring_size(self, size):
        self.circle_size = size

        self.resize(
            size,
            size
        )

        self.save_settings()

        self.update()

    def set_ring_color(self, color):
        self.ring_color = color

        self.save_settings()

        self.update()


class SettingsWindow(QWidget):
    def __init__(self, highlighter):
        super().__init__()

        self.highlighter = highlighter

        self.setWindowTitle(
            "Cursor Highlighter Settings"
        )

        self.resize(
            320,
            180
        )

        layout = QVBoxLayout()

        color_button = QPushButton(
            "Choose Ring Color"
        )

        color_button.clicked.connect(
            self.choose_color
        )

        layout.addWidget(
            color_button
        )

        layout.addWidget(
            QLabel("Ring Size")
        )

        self.slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.slider.setMinimum(40)
        self.slider.setMaximum(200)

        self.slider.setValue(
            self.highlighter.circle_size
        )

        self.slider.valueChanged.connect(
            self.change_size
        )

        layout.addWidget(
            self.slider
        )

        self.setLayout(
            layout
        )

    def choose_color(self):
        color = QColorDialog.getColor(
            self.highlighter.ring_color,
            self
        )

        if color.isValid():
            self.highlighter.set_ring_color(
                color
            )

    def change_size(self, value):
        self.highlighter.set_ring_size(
            value
        )

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event):
        event.ignore()
        self.hide()


app = QApplication(sys.argv)

app.setQuitOnLastWindowClosed(False)

highlighter = CursorHighlighter()

settings_window = SettingsWindow(
    highlighter
)


def trigger_highlight():
    QTimer.singleShot(
        0,
        highlighter.show_for_five_seconds
    )


def open_settings():
    QTimer.singleShot(
        0,
        settings_window.show_window
    )


keyboard.add_hotkey(
    "ctrl+shift+alt+z",
    trigger_highlight
)

keyboard.add_hotkey(
    "ctrl+alt+q",
    open_settings
)

highlighter.log("Hotkeys registered")

sys.exit(app.exec())
