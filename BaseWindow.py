from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout


class BaseWindow(QWidget):
    def __init__(self, title, image_path):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedSize(1280, 800)
        self.image_path = image_path

        # Set the background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor('#2E3B5B'))
        self.setPalette(palette)

        # Create a vertical layout for the whole window
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Create the custom title bar and add it to the layout
        self.titleBar = CustomTitleBar()
        self.main_layout.addWidget(self.titleBar)  # Add the title bar to the layout

        self.moving = False
        self.offset = None

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.windows = {}

        # close button
        button = QPushButton("X", self)
        button.setStyleSheet("color: rgba(255, 255, 255, 255);background-color: #2E3B5B; font-size: 18px;")
        button.setFixedSize(30, 30)
        button.move(1240, 12)
        button.clicked.connect(self.close)

    def navigate_to(self, window_class):
        if window_class not in self.windows or not self.windows[window_class].isVisible():
            self.windows[window_class] = window_class()
            self.windows[window_class].show()
            self.close()

    def setup_buttons(self, text, location, size, slot):
        button = QPushButton(text, self)
        button.setStyleSheet("color: rgba(255, 255, 255, 0);background-color: transparent; font-size: 18px;")
        button.setFixedSize(*size)
        button.move(*location)
        button.clicked.connect(slot)

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        print(f"Mouse Clicked at: ({x}, {y})")

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.image_path)
        painter.drawPixmap(self.rect(), pixmap)

    def closeEvent(self, event):
        # Perform any cleanup or save state if necessary
        event.accept()


class CustomTitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.offset = None
        self.moving = None
        self.initUI()

    def initUI(self):
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)

    def onClose(self):
        self.window().close()

    # def mousePressEvent(self, event):
    #     x, y = event.x(), event.y()
    #     if y < 20:
    #         if event.button() == Qt.LeftButton:
    #             self.parent().moving = True
    #             self.parent().offset = event.pos()

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        if y < 20:
            if self.parent().moving:
                self.parent().move(event.globalPos() - self.parent().offset)
