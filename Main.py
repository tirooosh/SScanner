import sys

from PyQt5.QtWidgets import QApplication

from hub import MainWindow
from PTestToolWindow import PTestToolWindow
from Loging_in import SignInWindow, SignUpWindow

# Main execution
app = QApplication(sys.argv)
window = MainWindow()
# window =SignUpWindow()
window.show()
sys.exit(app.exec_())
