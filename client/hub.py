from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea
from BaseWindow import BaseWindow, CustomTitleBar


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__("Main", "pictures\\main.png")
        self.setup_buttons("Sign in", (950, 350), (160, 200), self.go_to_sign_in)
        self.setup_buttons("About", (1100, 690), (140, 50), lambda: self.navigate_to(AboutWindow))
        self.setup_buttons("Sing up", (500, 345), (160, 200), self.go_to_sign_up)

        self.sign_in_window = None
        self.sign_up_window = None

    def go_to_sign_in(self):
        from Loging_in import SignInWindow
        # Check if the SignInWindow instance exists
        self.navigate_to(SignInWindow)

    def go_to_sign_up(self):
        from Loging_in import SignUpWindow
        # Check if the SignInWindow instance exists
        self.navigate_to(SignUpWindow)


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(1280, 800)
        self.image_path = "pictures\\about.png"

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor('#2E3B5B'))
        self.setPalette(palette)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.titleBar = CustomTitleBar()
        self.main_layout.addWidget(self.titleBar)

        self.moving = False
        self.offset = None

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(False)
        self.scroll.setStyleSheet("background: transparent;")

        # Scrollable Content
        content = QWidget()
        content_layout = QVBoxLayout(content)

        # QLabel for the image
        self.image_label = QLabel(content)
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap)
        content_layout.addWidget(self.image_label)

        self.scroll.setWidget(content)
        self.main_layout.addWidget(self.scroll)

        # Buttons and other widgets can be added here
        self.setup_buttons("Main", (996, 30), (250, 65), lambda: self.navigate_to(MainWindow))

        # Close button
        close_button = QPushButton("X", self)
        close_button.setStyleSheet("color: white; background-color: #2E3B5B; font-size: 18px; font-weight: 500;")
        close_button.setFixedSize(30, 30)
        close_button.move(1210, 12)
        close_button.clicked.connect(self.close)

        self.windows = {}

    def setup_buttons(self, text, location, size, slot):
        button = QPushButton(text, self)
        button.setStyleSheet("color: rgba(255, 255, 255, 0);background-color: transparent; font-size: 18px;")
        button.setFixedSize(*size)
        button.move(*location)
        button.clicked.connect(slot)

    def navigate_to(self, window_class):
        if window_class not in self.windows or not self.windows[window_class].isVisible():
            self.close()
            self.windows[window_class] = window_class()
            self.windows[window_class].show()
