from BaseWindow import BaseWindow
from PTestToolWindow import PTestToolWindow


class SignUpWindow(BaseWindow):
    def __init__(self):
        super().__init__("SignUp", "pictures\\signUp.png")
        self.setup_buttons("PTest Tool", (650, 675), (375, 50), lambda: self.navigate_to(PTestToolWindow))
        self.setup_buttons("Sign In", (915, 728), (80, 20), lambda: self.navigate_to(SignInWindow))
        self.setup_buttons("Main", (996, 30), (250, 65), self.go_to_main)

    def go_to_main(self):
        from hub import MainWindow
        self.navigate_to(MainWindow)


class SignInWindow(BaseWindow):
    def __init__(self):
        super().__init__("SignIn", "pictures\\signIn.png")
        self.setup_buttons("Sign Up", (905, 635), (80, 20), lambda: self.navigate_to(SignUpWindow))
        self.setup_buttons("Forgot Password", (905, 665), (165, 20), lambda: self.navigate_to(ForgotPasswordWindow))
        self.setup_buttons("PTest Tool", (660, 565), (375, 50), lambda: self.navigate_to(PTestToolWindow))
        self.setup_buttons("Main", (996, 30), (250, 65), self.go_to_main)

    def go_to_main(self):
        from hub import MainWindow
        self.navigate_to(MainWindow)


class ForgotPasswordWindow(BaseWindow):
    def __init__(self):
        super().__init__("Forgot password", "pictures\\forgotPassword.png")
        self.setup_buttons("Next", (660, 565), (375, 50), lambda: self.navigate_to(ForgotPassword2Window))
        self.setup_buttons("Main", (996, 30), (250, 65), self.go_to_main)

    def go_to_main(self):
        from hub import MainWindow
        self.navigate_to(MainWindow)


class ForgotPassword2Window(BaseWindow):
    def __init__(self):
        super().__init__("Forgot password", "pictures\\forgotPassword2.png")
        self.setup_buttons("Change Password", (660, 565), (375, 50), lambda: self.navigate_to(ChangePasswordWindow))
        self.setup_buttons("Main", (996, 30), (250, 65), self.go_to_main)

    def go_to_main(self):
        from hub import MainWindow
        self.navigate_to(MainWindow)


class ChangePasswordWindow(BaseWindow):
    def __init__(self):
        super().__init__("Change password", "pictures\\changePassword.png")
        self.setup_buttons("Sign In", (660, 565), (375, 50), lambda: self.navigate_to(SignInWindow))
        self.setup_buttons("Main", (996, 30), (250, 65), self.go_to_main)

    def go_to_main(self):
        from hub import MainWindow
        self.navigate_to(MainWindow)
