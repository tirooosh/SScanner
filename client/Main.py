import sys

from PyQt5.QtWidgets import QApplication

from hub import MainWindow
import client
from PTestToolWindow import PTestToolWindow
from Loging_in import SignInWindow, SignUpWindow
if client.check_server():
    # Main execution
    app = QApplication(sys.argv)
    window = MainWindow()
    # window =SignUpWindow()
    window.show()
    sys.exit(app.exec_())
else:
    print("the server is offline")
