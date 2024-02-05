from BaseWindow import BaseWindow
from hub import AboutWindow, MainWindow


class PTestToolWindow(BaseWindow):
    def __init__(self):
        super().__init__("Ptest tool", "pictures\\pTestTool.png")
        self.setup_buttons("About", (878, 74), (70, 20), lambda: self.navigate_to(AboutWindow))
        self.setup_buttons("History", (711, 74), (142, 20), lambda: self.navigate_to(AboutWindow))  # history
        self.setup_buttons("SignIn", (613, 74), (85, 20), lambda: self.navigate_to(MainWindow))  # logout
        self.setup_buttons("temp", (851, 377), (50, 50), lambda: self.navigate_to(AboutWindow))  # search

    def addSearchBar(self):
        self.s