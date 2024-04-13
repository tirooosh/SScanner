from PyQt5.QtWidgets import QLabel
from hub import AboutWindow, MainWindow
import client
from BaseWindow import BaseWindow
from PyQt5.QtWidgets import QLineEdit


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

    def show_results(self, sqlResults, xssResults, url):
        from resultWindow import ResultWindow
        final_results = {**sqlResults, **xssResults}
        try:
            self.navigate_to(ResultWindow, results=final_results, url=url)
        except:
            print("oops")

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
            sqlResults = sqlitest.run_tests(url)
            xssResults = xssiTest.run_tests(url)
            print("showing results")
            self.show_results(sqlResults, xssResults, url)
        else:
            print("Invalid URL")  # You might want to show this message in the GUI instead

    def validate_url(self, url):
        # Simple validation check, can be expanded based on requirements
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)
