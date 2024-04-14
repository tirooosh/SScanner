import threading
from queue import Queue

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
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

    def show_results(self, sqlResults, xssResults, url):
        final_results = {**sqlResults, **xssResults}
        self.navigate_to(ResultWindow, results=final_results, url=url)

    def navigate_to(self, window_class, *args, **kwargs):
        if window_class not in self.windows or not self.windows[window_class].isVisible():
            self.windows[window_class] = window_class(*args, **kwargs)
            self.windows[window_class].show()
        else:
            self.windows[window_class].activateWindow()  # Bring the window to the front if it's already open

    def Ptest(self):
        import sqlitest, xssiTest
        url = self.site_input.text()  # Get the text from QLineEdit

        if self.validate_url(url):

            results_queue = Queue()

            # Define a common method to handle thread execution and collect results
            def run_test(test_func):
                result = test_func()
                results_queue.put(result)

            self.navigate_to(LoadingScreens, email=self.email)
            # Start SQL test in a thread
            print("sqli test starting")
            sql_thread = threading.Thread(target=lambda: run_test(lambda: sqlitest.run_tests(url)))
            sql_thread.start()

            # Start XSS test in a thread
            print("xssi test starting")
            xss_thread = threading.Thread(target=lambda: run_test(lambda: xssiTest.run_tests(url)))
            xss_thread.start()

            print("loading...")
            self.showMinimized()


            # Wait for threads to complete and collect results
            sql_thread.join()
            xss_thread.join()

            # Extract results
            sqlResults = results_queue.get()
            xssResults = results_queue.get()

            # Now safely update the GUI with the results
            self.show_results(sqlResults, xssResults, url)
            self.showNormal()
        else:
            print("Invalid URL")  # You might want to show this message in the GUI instead

    def validate_url(self, url):
        # Simple validation check, can be expanded based on requirements
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)


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
        self.timer.start(2000)  # Set the timer to go off every 5 seconds

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

    def closeEvent(self, event):
        self.navigate_to(PTestToolWindow, email=self.email)
        event.accept()

    def mousePressEvent(self, event):
        pass
