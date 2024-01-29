import sys

from PyQt5.QtWidgets import QApplication

from gui import MainWindow

# Main execution
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())