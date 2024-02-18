from BaseWindow import BaseWindow
from PTestToolWindow import PTestToolWindow
from PyQt5.QtWidgets import QLineEdit
import re
import userdatabase
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SignUpWindow(BaseWindow):
    def __init__(self):
        super().__init__("SignUp", "pictures\\signUp.png")
        self.setup_buttons("PTest Tool", (650, 675), (375, 50), self.check_credentials)
        self.setup_buttons("Sign In", (915, 728), (80, 20), lambda: self.navigate_to(SignInWindow))
        self.setup_buttons("Main", (996, 30), (250, 65), self.go_to_main)

        # Name input field
        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(621, 251, 423, 53)
        self.name_input.setStyleSheet(
            "QLineEdit {"
            "   color: white;"  # Set text color to white
            "   background-color: transparent;"
            "   border: none;"  # Make border transparent
            "   font-size: 18px;"
            "}")

        # Email input field
        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(621, 347, 423, 53)
        self.email_input.setStyleSheet(
            "QLineEdit {"
            "   color: white;"  # Set text color to white
            "   background-color: transparent;"
            "   border: none;"  # Make border transparent
            "   font-size: 18px;"
            "}")

        # Password input field
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setGeometry(621, 441, 423, 53)
        self.password_input.setStyleSheet(
            "QLineEdit {"
            "   color: white;"  # Set text color to white
            "   background-color: transparent;"
            "   border: none;"  # Make border transparent
            "   font-size: 18px;"
            "}")

        # Repeat Password input field
        self.repeat_password_input = QLineEdit(self)
        self.repeat_password_input.setEchoMode(QLineEdit.Password)
        self.repeat_password_input.setGeometry(621, 534, 423, 53)
        self.repeat_password_input.setStyleSheet(
            "QLineEdit {"
            "   color: white;"  # Set text color to white
            "   background-color: transparent;"
            "   border: none;"  # Make border transparent
            "   font-size: 18px;"
            "}")

        self.setup_buttons("Show Password", (985, 455), (40, 40), self.show_password)

    def go_to_main(self):
        from hub import MainWindow
        self.navigate_to(MainWindow)

    def show_password(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            # If the password is currently hidden, show it
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            # If the password is currently shown, hide it
            self.password_input.setEchoMode(QLineEdit.Password)

    def check_credentials(self):
        # Get input values
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        repeat_password = self.repeat_password_input.text()

        # Validate email
        if not self.is_valid_email(email):
            print("Invalid email")
            return

        if len(password) < 6:
            print("Weak password")
            return

        # Check if passwords match
        if password != repeat_password:
            print("Passwords do not match")
            return

        # If all checks passed, proceed to the next window
        if userdatabase.signup(name, email, password):
            self.navigate_to(PTestToolWindow, email=email)

    def is_valid_email(self, email):
        # Basic email validation using regular expression
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(re.match(email_regex, email))


class SignInWindow(BaseWindow):
    def __init__(self):
        super().__init__("SignIn", "pictures\\signIn.png")
        self.setup_buttons("Sign Up", (905, 635), (80, 20), lambda: self.navigate_to(SignUpWindow))
        self.setup_buttons("Forgot Password", (905, 665), (165, 20), lambda: self.navigate_to(ForgotPasswordWindow))
        self.setup_buttons("PTest Tool", (660, 565), (375, 50), self.check_credentials)
        self.setup_buttons("Main", (996, 30), (250, 65), self.go_to_main)

        # email input field
        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(618, 266, 423, 53)
        self.email_input.setStyleSheet(
            "QLineEdit {"
            "   color: white;"  # Set text color to white
            "   background-color: transparent;"
            "   border: none;"  # Make border transparent
            "   font-size: 18px;"
            "}")

        # Password input field
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setGeometry(618, 378, 423, 53)
        self.password_input.setStyleSheet(
            "QLineEdit {"
            "   color: white;"  # Set text color to white
            "   background-color: transparent;"
            "   border: none;"  # Make border transparent
            "   font-size: 18px;"
            "}")

        self.setup_buttons("show password", (985, 380), (40, 40), self.show_password)

    def go_to_main(self):
        from hub import MainWindow
        self.navigate_to(MainWindow)

    def show_password(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            # If the password is currently hidden, show it
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            # If the password is currently shown, hide it
            self.password_input.setEchoMode(QLineEdit.Password)

    def check_credentials(self):
        email = self.email_input.text()
        password = self.password_input.text()
        can_login, str0 = userdatabase.login(email, password)
        if can_login:
            self.navigate_to(PTestToolWindow, email=email)
        else:
            print("not valid")


class ForgotPasswordWindow(BaseWindow):
    def __init__(self):
        super().__init__("Forgot password", "pictures\\forgotPassword.png")

        self.setup_buttons("Next", (660, 565), (375, 50), self.check_credentials)
        self.setup_buttons("Main", (996, 30), (250, 65), self.go_to_main)

        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(621, 336, 423, 53)
        self.email_input.setStyleSheet("""
            QLineEdit {
                color: white;
                background-color: transparent;
                border: none;
                font-size: 18px;
            }""")

    def check_credentials(self):
        email = self.email_input.text()
        if userdatabase.email_exists(email):  # Assuming `userdatabase` is a predefined object
            self.navigate_to(ForgotPassword2Window, email=email)
        else:
            print("Email not in system")

    def go_to_main(self):
        from hub import MainWindow
        self.navigate_to(MainWindow)


class ForgotPassword2Window(BaseWindow):
    def __init__(self, email):
        super().__init__("Forgot password", "pictures\\forgotPassword2.png")
        self.email = email
        self.setup_ui()
        self.send_reset_code()

    def setup_ui(self):
        self.setup_buttons("Change Password", (660, 565), (375, 50), self.check_credentials)
        self.setup_buttons("Main", (996, 30), (250, 65), self.go_to_main)

        # Generate and send reset code
        self.reset_code = str(random.randint(100000, 999999))

        self.confirmation_input = QLineEdit(self)
        self.confirmation_input.setGeometry(621, 336, 423, 53)
        self.confirmation_input.setStyleSheet("""
            QLineEdit {
                color: white;
                background-color: transparent;
                border: none;
                font-size: 18px;
            }""")

    def send_reset_code(self):
        try:

            sender_email = "tayouritirosh@gmail.com"
            app_password = "gyng opgk qpde hyge"  # Replace with your generated App Password
            subject = "Password Reset Code"
            body = f"Your password reset code is: {self.reset_code}"

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = self.email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, self.email, message.as_string())

            print(f"Reset code sent to {self.email}. Check your email.")
            response = {'message': 'Code sent successfully.'}
            return response
        except Exception as e:
            print(f"Error sending email: {e}")
            response = {'message': f'Failed to send reset code. Error: {str(e)}'}
            return response

    def check_credentials(self):
        confirmation_input = self.confirmation_input.text().strip()
        if self.reset_code == confirmation_input:
            self.navigate_to(ChangePasswordWindow, email=self.email)
        else:
            print("Incorrect code")

    def go_to_main(self):
        from hub import MainWindow
        self.navigate_to(MainWindow)


class ChangePasswordWindow(BaseWindow):
    def __init__(self, email):
        super().__init__("Change password", "pictures\\changePassword.png")
        self.email = email
        self.setup_buttons("Sign In", (660, 565), (375, 50), self.check_credentials)
        self.setup_buttons("Main", (996, 30), (250, 65), self.go_to_main)

        # Password input field
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setGeometry(621, 268, 423, 53)
        self.password_input.setStyleSheet(
            "QLineEdit {"
            "   color: white;"  # Set text color to white
            "   background-color: transparent;"
            "   border: none;"  # Make border transparent
            "   font-size: 18px;"
            "}")

        # Repeat Password input field
        self.repeat_password_input = QLineEdit(self)
        self.repeat_password_input.setEchoMode(QLineEdit.Password)
        self.repeat_password_input.setGeometry(621, 384, 423, 53)
        self.repeat_password_input.setStyleSheet(
            "QLineEdit {"
            "   color: white;"  # Set text color to white
            "   background-color: transparent;"
            "   border: none;"  # Make border transparent
            "   font-size: 18px;"
            "}")

        self.setup_buttons("Show Password", (985, 270), (40, 40), self.show_password)

    def show_password(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            # If the password is currently hidden, show it
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            # If the password is currently shown, hide it
            self.password_input.setEchoMode(QLineEdit.Password)

    def go_to_main(self):
        from hub import MainWindow
        self.navigate_to(MainWindow)

    def check_credentials(self):
        # Get input values
        password = self.password_input.text()
        repeat_password = self.repeat_password_input.text()

        if len(password) < 6:
            print("Weak password")
            return

        # Check if passwords match
        if password != repeat_password:
            print("Passwords do not match")
            return

        # If all checks passed, proceed to the next window
        is_changed, messege = userdatabase.change_password(self.email, password)
        if is_changed:
            print(messege)
            self.navigate_to(SignInWindow)
        else:
            print(messege)
