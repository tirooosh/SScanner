from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from BaseWindow import CustomTitleBar
import sys
import client
from resultWindow import ResultWindow


class HistoryWindow(QWidget):
    def __init__(self, email):
        super().__init__()
        self.setWindowTitle("History")
        self.setFixedSize(1280, 750)
        self.image_path = "pictures\\history.png"
        self.initUI(email)
        self.windows = {}

    def initUI(self, email):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor('#2E3B5B'))
        self.setPalette(palette)

        # Scrollable area setup
        self.scroll = QScrollArea(self)
        self.widget = QWidget()
        self.vbox = QVBoxLayout(self.widget)  # Layout for scrollable content
        self.vbox.setSpacing(0)  # No space between widgets
        self.vbox.setContentsMargins(0, 0, 0, 0)  # No margins around the layout

        # Adding custom title bar and image label
        self.titleBar = CustomTitleBar()
        self.vbox.addWidget(self.titleBar)

        self.image_label = QLabel()
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap)
        self.vbox.addWidget(self.image_label)

        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.scroll)

        # Scrollbar styling
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setStyleSheet("QScrollBar:vertical {background: #2E3B5B;}")

        # Close button
        close_button = QPushButton("X", self)
        close_button.setStyleSheet("color: white; background-color: #2E3B5B; font-size: 18px; font-weight: 500;")
        close_button.setFixedSize(30, 30)
        close_button.move(1210, 12)
        close_button.clicked.connect(self.close)

        self.setWindowFlags(Qt.FramelessWindowHint)

        results = client.get_results_from_user(email)
        self.add_buttons(results)  # Call separate function to add buttons

    def show_result(self, result):
        sqltest = result[1]
        xsstest = result[2]
        url = result[3]
        self.navigate_to(ResultWindow, sqltest=sqltest, xsstest=xsstest, url=url)

    def setup_buttons(self, text, location, size, slot):  # Not used in this fix
        # This function is no longer needed as we're using add_buttons
        pass

    def add_buttons(self, results):
        for i in range(len(results)):
            result = results[i]
            button_text = f"result number {i}"
            button_location = (935, 280 + (i * 70) + i)
            button_size = (280, 50)
            button = QPushButton(button_text, self.widget)
            button.setGeometry(button_location[0], button_location[1], button_size[0], button_size[1])
            button.clicked.connect(lambda result=result: self.show_result(result))  # Pass result as argument

            label_text1 = result[4]
            label_location1 = (10, 290 + (i * 70) + i)
            label_size1 = (190, 40)
            label1 = QLabel(label_text1, self.widget)
            label1.setGeometry(label_location1)
    def navigate_to(self, window_class, *args, **kwargs):
        if window_class not in self.windows or not self.windows[window_class].isVisible():
            self.windows[window_class] = window_class(*args, **kwargs)
            self.windows[window_class].show()
        else:
            self.windows[window_class].activateWindow()  # Bring the window to the front if it's already open    def navigate_to(self, window_class, *args, **kwargs):
        if window_class not in self.windows or not self.windows[window_class].isVisible():
            self.windows[window_class] = window_class(*args, **kwargs)
            self.windows[window_class].show()
        else:
            self.windows[window_class].activateWindow()  # Bring the window to the front if it's already open
