from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from BaseWindow import CustomTitleBar
import sys


class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("History")
        self.setFixedSize(1280, 800)
        self.image_path = "pictures\\history.png"
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor('#2E3B5B'))
        self.setPalette(palette)

        # Scrollable area setup
        self.scroll = QScrollArea(self)
        self.widget = QWidget()
        self.vbox = QVBoxLayout(self.widget)  # Parent vbox is the main layout holder for the scrollable widget

        # Adding custom title bar and image label
        self.titleBar = CustomTitleBar()
        self.vbox.addWidget(self.titleBar)

        self.image_label = QLabel()
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap)
        self.vbox.addWidget(self.image_label)

        # Adding buttons at specific positions within the scrollable area
        for i in range(24):
            self.setup_buttons(f"result number {i}", (935, 290 + (i * 70) + i), (280, 50))

        # Configure the scroll area
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.scroll)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def setup_buttons(self, text, location, size):
        button = QPushButton(text, self.widget)  # Note that parent is now self.widget
        button.setGeometry(location[0], location[1], size[0], size[1])  # Use setGeometry for absolute positioning


if __name__ == '__main__':
    app = QApplication(sys.argv)
    history = HistoryWindow()
    history.show()
    sys.exit(app.exec_())
