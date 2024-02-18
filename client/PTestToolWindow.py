from PyQt5.QtWidgets import QLabel
from hub import AboutWindow, MainWindow
import userdatabase
from BaseWindow import BaseWindow
from PyQt5.QtWidgets import QLineEdit


class PTestToolWindow(BaseWindow):
    def __init__(self, email):
        super().__init__("Ptest tool", "pictures\\pTestTool.png")
        self.setup_buttons("About", (878, 74), (70, 20), lambda: self.navigate_to(AboutWindow))
        self.setup_buttons("History", (711, 74), (142, 20), lambda: self.navigate_to(
            AboutWindow))  # Assuming this should navigate to a HistoryWindow instead
        self.setup_buttons("SignIn", (613, 74), (85, 20), lambda: self.navigate_to(
            MainWindow))  # Assuming this is for logout, consider renaming the button
        self.setup_buttons("search", (1035, 377), (50, 50),
                           self.Ptest)  # Assuming this is a placeholder for a future feature

        # Fetch the client's name using the provided email
        client_name = userdatabase.get_username(email)

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

    def Ptest(self):
        adress = self.site_input.text()
