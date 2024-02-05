import sys

from PyQt5.QtWidgets import QApplication

from hub import MainWindow
from PTestToolWindow import PTestToolWindow

# Main execution
app = QApplication(sys.argv)
window = PTestToolWindow()
# window = MainWindow()
window.show()
sys.exit(app.exec_())
