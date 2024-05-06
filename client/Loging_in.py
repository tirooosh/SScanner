from PyQt5.QtCore import QEvent

from BaseWindow import BaseWindow
from PTestToolWindow import PTestToolWindow
from PyQt5.QtWidgets import QLineEdit, QLabel
import re
import client
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
        self.setup_buttons("show reapet password", (985, 545), (40, 40), self.show_reapet_password)

        self.error_label = QLabel(self)
        self.error_label.setText("")
        self.error_label.setGeometry(620, 610, 2000, 60)
        self.error_label.setStyleSheet("""
            color: white;
            background-color: transparent;
            font-size: 20px;
            font-family: montserrat;
            font-weight: 500;
        """)

        # This is the label that users will hover over
        self.text_label = QLabel("(requirements)", self)
        self.text_label.setGeometry(1050, 455, 120, 20)
        self.text_label.setStyleSheet("font-size: 16px;color:yellow")

        # This is the label that appears when hovering over the text_label
        self.hover_label = QLabel("Password must contain at least 8 lowercase, uppercase, \nnumeric, and special characters (_, @, $, !, #, etc...)", self)
        self.hover_label.setGeometry(50, 200, 400, 40)
        self.hover_label.setStyleSheet("color: white; background-color: blue; font-size: 16px;")
        self.hover_label.hide()  # Initially hidden

        # Install a custom event filter on the text_label to catch hover events
        self.text_label.installEventFilter(self)

    def eventFilter(self, obj, event):
        # Check for mouse enter event
        if obj == self.text_label and event.type() == QEvent.Enter:
            self.hover_label.show()
            return True
        # Check for mouse leave event
        elif obj == self.text_label and event.type() == QEvent.Leave:
            self.hover_label.hide()
            return True
        return super().eventFilter(obj, event)

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

    def show_reapet_password(self):
        if self.repeat_password_input.echoMode() == QLineEdit.Password:
            # If the password is currently hidden, show it
            self.repeat_password_input.setEchoMode(QLineEdit.Normal)
        else:
            # If the password is currently shown, hide it
            self.repeat_password_input.setEchoMode(QLineEdit.Password)

    def check_credentials(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        repeat_password = self.repeat_password_input.text()

        def is_valid_email(email):
            try:
                # Simple regex for validating an Email
                pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                print(client.email_exists(email))
                if not client.email_exists(email) and re.match(pattern, email) is not None:
                    return True
                else:
                    return False

            except Exception as e:
                print(e)
            return False

        # Check for a valid email
        if not is_valid_email(email):
            self.error_label.setText("Invalid email.")
            return False

        # Password length check
        if len(password) < 8:
            self.error_label.setText("Password must be at least 8 characters.")
            return False

        # Password complexity check
        if not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]",
                                                                                                 password) or not re.search(
            "[_@$!#%*&]", password):
            self.error_label.setText(
                "Password must contain lowercase, uppercase, \nnumeric, and special characters (_, @, $, !, #, etc...).")
            return False

        # Passwords match check
        if password != repeat_password:
            self.error_label.setText("Passwords do not match.")
            return False

        # Username length check
        if len(name) < 2 or len(name) > 20:
            self.error_label.setText("The username must be between 2 and 20 characters.")
            return False

        # Password space check
        if " " in password:
            self.error_label.setText("Password cannot contain spaces.")
            return False

        # If all checks passed
        print("All inputs are valid.")

        try:
            success = client.signup(name, email, password)
            if success:
                self.navigate_to(SignInWindow)
        except Exception as e:
            print(f"Error during signup: {e}")


class SignInWindow(BaseWindow):
    def __init__(self):
        super().__init__("SignIn", "pictures\\signIn.png")
        self.setup_buttons("Sign Up", (905, 635), (90, 20), lambda: self.navigate_to(SignUpWindow))
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

        self.error_label = QLabel(self)
        self.error_label.setText("")
        self.error_label.setGeometry(660, 500, 2000, 30)
        self.error_label.setStyleSheet("""
                    color: white;
                    background-color: transparent;
                    font-size: 20px;
                    font-family: montserrat;
                    font-weight: 500;
                """)

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
        try:
            can_login, message = client.login(email, password)
            if can_login:
                self.navigate_to(PTestToolWindow, email=email)
            else:
                self.error_label.setText("not valid")
        except Exception as e:
            print(f"Error during login: {e}")


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

    def check_credentials(self):
        email = self.email_input.text()
        try:
            exist = client.email_exists(email)
            if exist:
                self.navigate_to(ForgotPassword2Window, email=email)
            else:
                self.error_label.setText("Email not in system")
        except Exception as e:
            print(f"Error checking email: {e}")

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

    def send_reset_code(self):
        try:

            sender_email = "tayouritirosh@gmail.com"
            app_password = "gyng opgk qpde hyge"  # generated App Password
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

            self.error_label.setText(f"Reset code sent to {self.email}. Check your email.")
            response = {'message': 'Code sent successfully.'}
            return response
        except Exception as e:
            self.error_label.setText(f"Error sending email: {e}")
            response = {'message': f'Failed to send reset code. Error: {str(e)}'}
            return response

    def check_credentials(self):
        confirmation_input = self.confirmation_input.text().strip()
        if self.reset_code == confirmation_input:
            self.navigate_to(ChangePasswordWindow, email=self.email)
        else:
            self.error_label.setText("Incorrect code")

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
        password = self.password_input.text()
        repeat_password = self.repeat_password_input.text()

        if len(password) < 6:
            self.error_label.setText("Weak password")
            return

        if password != repeat_password:
            self.error_label.setText("Passwords do not match")
            return

        try:
            is_changed = client.change_password(self.email, password)
            if is_changed:
                self.error_label.setText("sucssesfull")
                self.navigate_to(SignInWindow)
            else:
                self.error_label.setText("oopsy")
        except Exception as e:
            print(f"Error changing password: {e}")
