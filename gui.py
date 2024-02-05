from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
import sys


class BaseWindow(QWidget):
    def __init__(self, title, image_path):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedSize(1280, 800)

        # Use QVBoxLayout as the main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Set background image using stylesheet with no-repeat
        self.setStyleSheet(f"background-image: url({image_path}); background-repeat: no-repeat;")

        # Example QLabel with an image
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        self.main_layout.addWidget(image_label)

        # Create an attribute to hold the Windows instance
        self.sign_in_window = None
        self.sign_up_window = None
        self.about_window = None
        self.forgot_password_window = None

    def add_transparent_button(self, text, slot):
        button = QPushButton(text)
        button.setFlat(True)
        button.setStyleSheet("color: white; background-color: transparent; border: none; font-size: 18px;")
        button.clicked.connect(slot)
        self.main_layout.addWidget(button)

    def go_to_sign_in(self):
        # Check if the SignInWindow instance exists
        if not self.sign_in_window or not self.sign_in_window.isVisible():
            self.sign_in_window = SignInWindow()
            self.sign_in_window.show()

    def go_to_sign_up(self):
        # Check if the SignInWindow instance exists
        if not self.sign_up_window or not self.sign_up_window.isVisible():
            self.sign_up_window = SignUpWindow()
            self.sign_up_window.show()

    def go_to_about(self):
        # Check if the SignInWindow instance exists
        if not self.about_window or not self.about_window.isVisible():
            self.about_window = AboutWindow()
            self.about_window.show()

    def go_to_forgot_password(self):
        # Check if the forgotpassword instance exists
        if not self.forgot_password_window or not self.forgot_password_window.isVisible():
            self.forgot_password_window = ForgotPasswordWindow()
            self.forgot_password_window.show()


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__("Main", "C:/cyber 2024/tirosh/pics/main.png")
        # Transparent buttons
        self.add_transparent_button("SignIn", self.go_to_sign_in)
        self.add_transparent_button("SignUp", self.go_to_sign_up)
        self.add_transparent_button("About", self.go_to_about)


class SignUpWindow(BaseWindow):
    def __init__(self):
        super().__init__("SignUp", "C:/cyber 2024/tirosh/pics/signUp.png")
        # Transparent buttons
        self.add_transparent_button("SignIn", self.go_to_sign_in)
        self.add_transparent_button("SignIn", self.go_to_forgot_password())


class SignInWindow(BaseWindow):
    def __init__(self):
        super().__init__("SignIn", "C:/cyber 2024/tirosh/pics/signIn.png")
        self.add_transparent_button("SignUp", self.go_to_sign_up)
        self.add_transparent_button("SignIn", self.go_to_forgot_password())


class PTestToolWindow(BaseWindow):
    def __init__(self):
        super().__init__("Ptest tool", "C:/cyber 2024/tirosh/pics/pTestTool.png")


class AboutWindow(BaseWindow):
    def __init__(self):
        super().__init__("About", "C:/cyber 2024/tirosh/pics/about.png")


class HistoryWindow(BaseWindow):
    def __init__(self):
        super().__init__("History", "C:/cyber 2024/tirosh/pics/history.png")


class ChangePasswordWindow(BaseWindow):
    def __init__(self):
        super().__init__("Change password", "C:/cyber 2024/tirosh/pics/changePassword.png")


class ForgotPasswordWindow(BaseWindow):
    def __init__(self):
        super().__init__("Forgot password", "C:/cyber 2024/tirosh/pics/forgotPassword.png")


class ForgotPassword2Window(BaseWindow):
    def __init__(self):
        super().__init__("Forgot password", "C:/cyber 2024/tirosh/pics/forgotPassword2.png")


app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
sys.exit(app.exec_())
