from functools import partial

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
        self.windows = {}

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
        # Scale pixmap to the current label's size
        scaled_pixmap = pixmap.scaled(self.width() - 41, self.height(), Qt.KeepAspectRatioByExpanding)
        self.image_label.setPixmap(scaled_pixmap)
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
        if not results:  # Check if results are empty
            print("No results available.")
            return  # Optionally, add some UI feedback here
        btnLst = []
        if email == "tiroshtayouri@gmail.com":
            results = client.get_all_test_results()
        for i, result in enumerate(results):
            btnLst.append(self.setup_buttons(
                f"result number {i}",
                (935, 280 + (i * 70) + i),
                (280, 50)))
            self.add_label(result[4], (10, 290 + (i * 70) + i), (190, 40))
            self.add_label(result[3], (220, 290 + (i * 70) + i), (630, 40))

        self.connect_slot(results, btnLst)

        username = str(client.get_username(email))
        self.add_label(username, (130, 105), (300, 50))

    def connect_slot(self, results, btnLst):
        try:
            for counter, button in enumerate(btnLst):
                result = results[counter]
                button.clicked.connect(partial(self.show_result, result))
        except Exception as e:
            print(e)

    def show_result(self, result):
        sqltest = result[1]
        xsstest = result[2]
        url = result[3]
        self.navigate_to(ResultWindow, sqltest=sqltest, xsstest=xsstest, url=url)

    def setup_buttons(self, text, location, size):
        button = QPushButton(text, self.widget)  # Note that parent is now self.widget
        button.setGeometry(location[0], location[1], size[0], size[1])  # Use setGeometry for absolute positioning
        return button

    def add_label(self, text, location, size):
        lable = QLabel(text, self.widget)
        lable.setGeometry(location[0], location[1], size[0], size[1])
        lable.setStyleSheet("color: white; background-color: #2E3B5B; font-size: 18px; font-weight: 500;")

    def open_result_window(self, sqltest, xsstest, url):
        print(sqltest, xsstest, url)
        try:
            resultWin = ResultWindow(sqltest, xsstest, url)
            resultWin.show()
        except Exception as e:
            print(e)

    def navigate_to(self, window_class, *args, **kwargs):
        if window_class not in self.windows or not self.windows[window_class].isVisible():
            self.windows[window_class] = window_class(*args, **kwargs)
            self.windows[window_class].show()
        else:
            self.windows[window_class].activateWindow()  # Bring the window to the front if it's already open


if __name__ == '__main__':
    app = QApplication(sys.argv)
    history = HistoryWindow("user123@gmail.com")
    history.show()
    sys.exit(app.exec_())
