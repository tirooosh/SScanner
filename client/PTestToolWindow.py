import threading
from queue import Queue

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtWidgets import QLineEdit

import client
from BaseWindow import BaseWindow
from hub import AboutWindow, MainWindow
from resultWindow import ResultWindow


class PTestToolWindow(BaseWindow):
    def __init__(self, email):
        super().__init__("Ptest tool", "pictures\\pTestTool.png")
        self.setup_buttons("About", (878, 74), (70, 20), lambda: self.navigate_to(AboutWindow))
        self.setup_buttons("History", (711, 74), (142, 20), lambda: self.navigate_to(
            AboutWindow))  # Assuming this should navigate to a HistoryWindow instead
        self.setup_buttons("main", (613, 74), (85, 20), lambda: self.navigate_to(
            MainWindow))  # Assuming this is for logout, consider renaming the button
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

    def prepare_show_results(self, sqlResults, xssResults, url):
        try:
            client.add_test_result(test1=sqlResults, test2=xssResults, url=url,
                               username_of_searcher=self.email)
        except Exception as e:
            print(f"Error sending data: {e}")
        self.close_all_specific_type_windows(LoadingScreens)
        self.showNormal()
        self.show_results(xssResults, sqlResults, url)

    def navigate_to(self, window_class, *args, **kwargs):
        if window_class not in self.windows or not self.windows[window_class].isVisible():
            self.windows[window_class] = window_class(*args, **kwargs)
            self.windows[window_class].show()
        else:
            self.windows[window_class].activateWindow()  # Bring the window to the front if it's already open

    def Ptest(self):
        import sqlitest, xssiTest
        url = self.site_input.text()  # Get the text from QLineEdit
        self.site_input.clear()
        if self.validate_url(url):
            results_queue = Queue()

            def run_test(test_func, func_arg):
                result = test_func(func_arg)
                results_queue.put(result)

            # Navigate to loading screen before starting tests
            self.navigate_to(LoadingScreens, email=self.email)

            # Start SQL and XSS tests in separate threads
            sql_thread = threading.Thread(target=lambda: run_test(sqlitest.run_tests, url))
            sql_thread.start()
            xss_thread = threading.Thread(target=lambda: run_test(xssiTest.run_tests, url))
            xss_thread.start()

            # Check the threads in intervals without blocking main thread
            self.check_threads(sql_thread, xss_thread, results_queue)
        else:
            print("Invalid URL")

    def check_threads(self, sql_thread, xss_thread, results_queue):
        if sql_thread.is_alive() or xss_thread.is_alive():
            # Recheck in 100 ms
            QTimer.singleShot(100, lambda: self.check_threads(sql_thread, xss_thread, results_queue))
        else:
            # Threads have completed
            sqlResults = results_queue.get()
            xssResults = results_queue.get()
            sql_thread.join()
            xss_thread.join()
            self.prepare_show_results(sqlResults, xssResults, self.site_input.text())
            self.showNormal()  # Restore the main window

    def validate_url(self, url):
        # Simple validation check, can be expanded based on requirements
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)

    def close_all_specific_type_windows(self, clas):
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, clas):
                widget.close()


    def show_results(self, test1, test2, url):
        print("showing results for", test1, test2, url)
        try:
            res = ResultWindow(test1, test2, url=url)
            res.show()
        except Exception as e:
            print(e)


class LoadingScreens(BaseWindow):
    def __init__(self, email):
        super().__init__("loading screen", f"pictures\\loadingscreen ({1}).png")
        self.email = email
        self.image_index = 0  # Start with the first image
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Loading Screen')

        self.label = QLabel(self)  # Create a label to show the images
        self.label.resize(1280, 800)  # Set label size
        self.update_image()

        self.timer = QTimer(self)  # Create a QTimer
        self.timer.timeout.connect(self.update_image)  # Connect timeout to the update_image method
        self.timer.start(35000)  # second = 1000

    def update_image(self):
        images = [
            "pictures\\loadingscreen (2).png",
            "pictures\\loadingscreen (3).png",
            "pictures\\loadingscreen (4).png",
            "pictures\\loadingscreen (5).png"
        ]
        if self.image_index < len(images):
            self.label.setPixmap(QPixmap(images[self.image_index]))  # Update the label with new image
            self.image_index += 1
        else:
            self.timer.stop()  # Stop the timer if all images have been displayed
            self.label.setPixmap(QPixmap("pictures\\loadingscreen (5).png"))

    def mousePressEvent(self, event):
        pass


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)  # Initialize the QApplication

    email = "temp"
    test1 = 2
    test2 = 2
    url = "http://example.com/result1"
    username_of_searcher = "tirosh"

    ptest_window = PTestToolWindow(email)
    ptest_window.show()  # Show the main window

    # client.add_test_result(test1=test1, test2=test2, url=url,
    #                        username_of_searcher=client.get_username(email))
    # # Simulate the test results being ready
    res = ResultWindow(test1, test2, url=url)
    res.show()
    ptest_window.prepare_show_results(test1, test2, url)
    sys.exit(app.exec_())  # Start the event loop
