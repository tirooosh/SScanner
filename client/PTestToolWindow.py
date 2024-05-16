import threading
from queue import Queue
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtWidgets import QLineEdit

import client
from BaseWindow import BaseWindow
from hub import AboutWindow, MainWindow
from resultWindow import ResultWindow
from historyWindow import HistoryWindow
from PyQt5.QtGui import QPixmap, QPainter, QTransform


class PTestToolWindow(BaseWindow):
    def __init__(self, email):
        super().__init__("Ptest tool", "pictures\\pTestTool.png")
        self.setup_buttons("About", (878, 74), (70, 20), lambda: self.navigate_to(AboutWindow))
        self.setup_buttons("History", (711, 74), (142, 20), lambda: self.show_history(
            email=email))
        self.setup_buttons("Log_out", (613, 74), (85, 20), lambda: self.logout(
            MainWindow))
        self.setup_buttons("search", (1035, 377), (50, 50),
                           self.Ptest)  # Assuming this is a placeholder for a future feature

        # Fetch the client's name using the provided email
        client_name = client.get_username(email)

        # Create and configure the label to display the client's name
        self.client_name_label = QLabel(self)
        self.client_name_label.setText("Hello " + client_name)
        self.client_name_label.setGeometry(135, 80, 200, 30)
        self.client_name_label.setStyleSheet("""
            color: black;
            background-color: transparent;
            font-size: 20px;
            font-family: montserrat;
            font-weight: 500;
        """)

        self.site_input = QLineEdit(self)
        self.site_input.setGeometry(267, 370, 750, 63)
        self.site_input.setStyleSheet(
            "QLineEdit {"
            "   color: black;"  # Set text color to black
            "   background-color: transparent;"
            "   border: none;"  # Make border transparent
            "   font-size: 18px;"
            "}")
        self.email = email

        self.error_label = QLabel(self)
        self.error_label.setText("")
        self.error_label.setGeometry(660, 640, 2000, 30)
        self.error_label.setStyleSheet("""
                    color: white;
                    background-color: transparent;
                    font-size: 20px;
                    font-family: montserrat;
                    font-weight: 500;
                """)

    def logout(self, window_class, *args, **kwargs):
        self.navigate_to(window_class, *args, **kwargs)
        self.close()

    def navigate_to(self, window_class, *args, **kwargs):
        if window_class not in self.windows or not self.windows[window_class].isVisible():
            self.windows[window_class] = window_class(*args, **kwargs)
            self.windows[window_class].show()
        else:
            self.windows[window_class].activateWindow()  # Bring the window to the front if it's already open

    def show_history(self, email):
        try:
            win = HistoryWindow(email)
            win.show()
        except Exception as e:
            print(e)

    def Ptest(self):
        import sqlitest, xssiTest
        url = self.site_input.text()  # Get the text from QLineEdit
        if self.validate_url(url):
            results_queue = Queue()
            self.site_input.clear()

            def run_test(test_func, func_arg):
                result = test_func(func_arg)
                results_queue.put(result)

            # Navigate to loading screen before starting tests
            self.navigate_to(LoadingScreens, email=self.email)

            fast_results = client.get_results_from_url(url)
            if fast_results is not None:
                sqlResults = fast_results[0]
                xssResults = fast_results[1]
                print(sqlResults, xssResults, url)
                self.prepare_show_results(sqlResults, xssResults, url)
            else:
                # Start SQL and XSS tests in separate threads
                sql_thread = threading.Thread(target=lambda: run_test(sqlitest.run_tests, url))
                sql_thread.start()
                xss_thread = threading.Thread(target=lambda: run_test(xssiTest.run_tests, url))
                xss_thread.start()

                # Check the threads in intervals without blocking main thread
                self.check_threads(sql_thread, xss_thread, results_queue, url)
        else:
            self.error_label.setText("Invalid URL")

    def check_threads(self, sql_thread, xss_thread, results_queue, url):
        if sql_thread.is_alive() or xss_thread.is_alive():
            # Recheck in 100 ms
            QTimer.singleShot(100, lambda: self.check_threads(sql_thread, xss_thread, results_queue, url))
        else:
            # Threads have completed
            sqlResults = results_queue.get()
            xssResults = results_queue.get()
            sql_thread.join()
            xss_thread.join()
            self.prepare_show_results(sqlResults, xssResults, url)

    def validate_url(self, url):
        # Simple validation check, can be expanded based on requirements
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)

    def prepare_show_results(self, sqlResults, xssResults, url):
        try:
            client.add_test_result(test1=sqlResults, test2=xssResults, url=url, email_of_searcher=self.email)
            self.show_results(sqlResults, xssResults, url)
        except Exception as e:
            print(f"Error sending data: {e}")
        self.close_all_specific_type_windows(LoadingScreens)

    def show_results(self, sqlResults, xssResults, url):
        self.navigate_to(ResultWindow, sqltest=sqlResults, xsstest=xssResults, url=url)
        self.showNormal()

    def close_all_specific_type_windows(self, clas):
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, clas):
                widget.close()


class LoadingScreens(BaseWindow):
    def __init__(self):
        super().__init__("Loading Screen", "pictures\\loadingscreen.png")
        self.num_legs = 0  # Number of legs displayed (each pair counts as two)
        self.leg_spacing = 50  # Horizontal space between legs
        self.x_pos = 400  # Starting x position for the first leg
        self.x_increment = 30  # Increment for x position of the second leg in each pair
        self.max_legs = 19  # Maximum number of legs
        self.adding_second_leg = False  # Track if adding second leg in pair

        # Calculate appropriate pixmap dimensions
        self.pixmap = QPixmap(self.width(), self.height())
        self.pixmap.fill(Qt.transparent)  # Initialize pixmap as transparent

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Loading Screen')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_legs)
        self.timer.start(500)  # Start with 500 milliseconds for the first leg

    def add_legs(self):
        if self.num_legs < self.max_legs:
            base_x_position = self.x_pos + (self.num_legs // 2) * self.leg_spacing
            y_position = 635 if not self.adding_second_leg else 652
            x_position = base_x_position if not self.adding_second_leg else base_x_position + self.x_increment
            scale = 0.4

            self.draw_leg(x_position, y_position, scale)
            self.num_legs += 1
            self.update()  # Redraw window

            if not self.adding_second_leg:
                self.adding_second_leg = True
                self.timer.start(500)  # Same delay for the second leg
            else:
                self.adding_second_leg = False
                self.timer.start(1000)  # Twice the delay before the next set
        else:
            self.reset_animation()

    def reset_animation(self):
        self.pixmap.fill(Qt.transparent)  # Clear the pixmap
        self.num_legs = 0  # Reset the leg counter
        self.adding_second_leg = False  # Reset leg pair state
        self.timer.start(500)  # Restart the timer

    def draw_leg(self, x, y, scale):
        leg_pixmap = QPixmap("pictures\\etc\\duck_legs.png")
        if leg_pixmap.isNull():
            print("Failed to load leg image")
            return
        # Scale down the pixmap
        transform = QTransform().scale(scale, scale)
        scaled_pixmap = leg_pixmap.transformed(transform, Qt.SmoothTransformation)
        painter = QPainter(self.pixmap)
        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()

    def paintEvent(self, event):
        super().paintEvent(event)  # Ensure background is painted
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)  # Draw the legs pixmap

    def mousePressEvent(self, event):
        pass


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)  # Initialize the QApplication

    email = "temp"
    sqlResults = 2
    xssResults = 2
    url = "http://example.com/result1"
    username_of_searcher = "tirosh"

    ptest_window = PTestToolWindow(email)
    ptest_window.show()  # Show the main window

    sys.exit(app.exec_())  # Start the event loop
